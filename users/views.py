from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile, Skill, Message
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import *

# Create your views here.


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'Username does not exist')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User successfully logged in')
            return redirect(request.GET['next'] if 'next' in request.GET else 'user-profile',
                            pk=request.user.profile.id)

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):

    if request.user.is_authenticated == False:
        return redirect('login')

    logout(request)
    messages.info(request, 'User successfully logged out')
    return redirect('login')


def signUp(request):

    if request.user.is_authenticated:
        return redirect('/')

    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Account successfully created!')
            login(request, user)
            return redirect('edit-profile')

        else:
            messages.success(request, 'An error occurred during registration')

    context ={'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchDevelopers(request)

    profiles, custom_page_range = profiles_paginator(request, profiles, 6)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_page_range': custom_page_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    description_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")

    context = {'profile': profile}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user-profile', profile.id)

    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


@login_required(login_url='login')
def add_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = profile
            form.save()
            messages.success(request, 'Skill added successfully')

            return redirect('user-profile', profile.id)

    context = {'form': form}
    return render(request, 'users/add_skill.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill changed successfully')

            return redirect('user-profile', profile.id)

    context = {'form': form}
    return render(request, 'users/add_skill.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully')
        return redirect('user-profile', profile.id)

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


def send_message(request, pk):
    receiver = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.sender = sender
            form.receiver = receiver

            if sender:
                form.name = sender.name
                form.email = sender.email

            form.save()

            messages.success(request, 'Message Delivered')
            return redirect('user-profile', receiver.id)

        else:
            messages.error(request, 'An error occurred')

    context = {'receiver': receiver, 'form': form}
    return render(request, 'users/send_message.html', context)


@login_required(login_url='login')
def chat_inbox(request):
    profile = request.user.profile
    user_messages = profile.messages.all()
    user_unread_messages_count = user_messages.filter(is_seen=False).count()
    context = {'user_messages': user_messages, 'user_unread_messages_count': user_unread_messages_count}
    return render(request, 'users/messages.html', context)


@login_required(login_url='login')
def inbox_detail(request, pk):
    profile = request.user.profile
    message_obj = profile.messages.get(id=pk)
    if message_obj.is_seen == False:
        message_obj.is_seen = True
        message_obj.save()
    context = {'message_obj': message_obj}
    return render(request, 'users/message_detail.html', context)
