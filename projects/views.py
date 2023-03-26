from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from .utils import search_projects, projects_paginator


def projects(request):
    projects, search_query = search_projects(request)

    projects, custom_page_range = projects_paginator(request, projects, 6)

    context = {'projects': projects, 'search_query': search_query, 'custom_page_range': custom_page_range}

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.user = request.user.profile
        review.save()

        projectObj.get_vote_count

        messages.success(request, 'Your review was submitted successfully')
        return redirect('project', pk=projectObj.id)

    context = {'project': projectObj, 'form': form}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url="login")
def createProject(request):
    user = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.save()
            return redirect('user-profile', user.id)

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('user-profile', profile.id)

    context = {'form':form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('user-profile', profile.id)
    context = {'object': project}
    return render(request, 'delete_template.html', context)