from .models import Profile, Skill
from django.db.models import Q
from  django.core.paginator import *


def searchDevelopers(request):
    search_query = ''

    if request.GET.get('query'):
        search_query = request.GET.get('query')

    skills = Skill.objects.filter(name__icontains=search_query)

    # profiles = Profile.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(
        skill__in=skills)).distinct()

    return profiles, search_query


def profiles_paginator(request, profiles, results):

    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page) - 4)

    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_page_range = range(left_index, right_index)

    return profiles, custom_page_range


