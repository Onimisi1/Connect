from .models import Project, Tag
from django.db.models import Q
from  django.core.paginator import *


def search_projects(request):
    search_query = ''

    if request.GET.get('query'):
        search_query = request.GET.get('query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(user__name__icontains=search_query) |
        Q(tags__in=tags)
    ).distinct()

    return projects, search_query


def projects_paginator(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    left_index = (int(page) - 4)

    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_page_range = range(left_index, right_index)

    return projects, custom_page_range
