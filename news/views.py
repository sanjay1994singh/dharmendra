# views.py

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import *


def home(request):
    news = News.objects.all().order_by('-id')

    paginator = Paginator(news, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    latest_news = News.objects.all().order_by('-id')[:1]

    trending_news = News.objects.all().order_by('-count')[:8]

    breaking_news = News.objects.all().order_by('-id')[:10]

    categories = Category.objects.all()

    category_news = []

    for category in categories:
        category_news.append({

            'category': category,

            'news': News.objects.filter(
                category=category
            ).order_by('-id')[:10]

        })

    context = {

        'page_obj': page_obj,

        'latest_news': latest_news,

        'trending_news': trending_news,

        'breaking_news': breaking_news,

        'category_news': category_news,

    }

    return render(
        request,
        'index.html',
        context
    )


def news_detail(request, id):
    news = get_object_or_404(
        News,
        id=id
    )

    news.count += 1

    news.save()

    related_news = News.objects.filter(
        category=news.category
    ).exclude(id=id).order_by('-id')[:6]

    context = {

        'news': news,

        'related_news': related_news,

    }

    return render(
        request,
        'news_detail.html',
        context
    )


def category_news(request, id):
    category = get_object_or_404(
        Category,
        id=id
    )

    news = News.objects.filter(
        category=category
    ).order_by('-id')

    paginator = Paginator(news, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {

        'selected_category': category,

        'page_obj': page_obj,

    }

    return render(
        request,
        'category_news.html',
        context
    )


def load_more_news(request, id):
    category = get_object_or_404(
        Category,
        id=id
    )

    page = request.GET.get('page', 1)

    news = News.objects.filter(
        category=category
    ).order_by('-id')

    paginator = Paginator(news, 10)

    page_obj = paginator.get_page(page)

    data = []

    for item in page_obj:
        data.append({

            'id': item.id,

            'title': item.title,

            'text': item.text[:120],

            'image': item.featured_image.url if item.featured_image else ''

        })

    return JsonResponse({

        'data': data,

        'has_next': page_obj.has_next()

    })
