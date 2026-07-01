# views.py

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.html import strip_tags
from xml.sax.saxutils import escape
import json

from .models import *


SITE_NAME = 'News Fast Live'
SITE_DESCRIPTION = (
    'News Fast Live brings latest Hindi news, breaking updates, politics, '
    'religious, education, crime and local stories.'
)


def absolute_url(request, view_name, *args):
    return request.build_absolute_uri(reverse(view_name, args=args))


def clean_description(value, length=160):
    return strip_tags(value or '').replace('\n', ' ').strip()[:length]


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

        'seo_title': f'{SITE_NAME} - Latest Hindi News, Breaking News and Updates',

        'seo_description': SITE_DESCRIPTION,

        'seo_canonical': request.build_absolute_uri(reverse('home')),

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

    # increase views

    news.count += 1

    news.save()

    # related news

    related_news = News.objects.filter(
        category=news.category
    ).exclude(
        id=id
    ).order_by('-id')[:6]

    # absolute image url

    absolute_image_url = ''

    if news.featured_image:

        absolute_image_url = request.build_absolute_uri(
            news.featured_image.url
        )

    article_url = absolute_url(request, 'news_detail', news.id)

    article_schema = {
        '@context': 'https://schema.org',
        '@type': 'NewsArticle',
        'headline': news.title or SITE_NAME,
        'description': clean_description(news.text, 180),
        'mainEntityOfPage': {
            '@type': 'WebPage',
            '@id': article_url,
        },
        'datePublished': news.created_at.isoformat() if news.created_at else '',
        'dateModified': news.updated_at.isoformat() if news.updated_at else '',
        'author': {
            '@type': 'Person',
            'name': news.reporter or SITE_NAME,
        },
        'publisher': {
            '@type': 'Organization',
            'name': SITE_NAME,
        },
    }

    if absolute_image_url:
        article_schema['image'] = [absolute_image_url]

    context = {

        'news': news,

        'related_news': related_news,

        'absolute_image_url': absolute_image_url,

        'seo_title': f'{news.title} | {SITE_NAME}',

        'seo_description': clean_description(news.text, 160),

        'seo_canonical': article_url,

        'seo_image': absolute_image_url,

        'og_type': 'article',

        'article_schema': json.dumps(article_schema, ensure_ascii=False),

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

        'seo_title': f'{category.name} News | {SITE_NAME}',

        'seo_description': clean_description(
            category.desc,
            160
        ) or f'Latest {category.name} news and updates on {SITE_NAME}.',

        'seo_canonical': absolute_url(request, 'category_news', category.id),

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

            'text': strip_tags(item.text or '')[:120],

            'image': item.featured_image.url if item.featured_image else ''

        })

    return JsonResponse({

        'data': data,

        'has_next': page_obj.has_next()

    })


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse('sitemap_xml'))
    content = '\n'.join([
        'User-agent: *',
        'Allow: /',
        f'Sitemap: {sitemap_url}',
        '',
    ])
    return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
    urls = [
        {
            'loc': request.build_absolute_uri(reverse('home')),
            'lastmod': '',
            'priority': '1.0',
            'changefreq': 'hourly',
        }
    ]

    for category in Category.objects.all().order_by('id'):
        urls.append({
            'loc': absolute_url(request, 'category_news', category.id),
            'lastmod': category.updated_at.date().isoformat() if category.updated_at else '',
            'priority': '0.8',
            'changefreq': 'daily',
        })

    for item in News.objects.all().order_by('-updated_at', '-id'):
        image_url = ''
        if item.featured_image:
            image_url = request.build_absolute_uri(item.featured_image.url)

        urls.append({
            'loc': absolute_url(request, 'news_detail', item.id),
            'lastmod': item.updated_at.date().isoformat() if item.updated_at else '',
            'priority': '0.9',
            'changefreq': 'daily',
            'image': image_url,
            'image_title': item.title or '',
        })

    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    for item in urls:
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{escape(item["loc"])}</loc>')

        if item.get('lastmod'):
            xml_parts.append(f'    <lastmod>{escape(item["lastmod"])}</lastmod>')

        xml_parts.append(f'    <changefreq>{item["changefreq"]}</changefreq>')
        xml_parts.append(f'    <priority>{item["priority"]}</priority>')

        if item.get('image'):
            xml_parts.append('    <image:image>')
            xml_parts.append(f'      <image:loc>{escape(item["image"])}</image:loc>')
            xml_parts.append(f'      <image:title>{escape(item["image_title"])}</image:title>')
            xml_parts.append('    </image:image>')

        xml_parts.append('  </url>')

    xml_parts.append('</urlset>')

    return HttpResponse('\n'.join(xml_parts), content_type='application/xml')


def rss_feed(request):
    items = News.objects.all().order_by('-id')[:50]
    site_url = request.build_absolute_uri(reverse('home'))

    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '<channel>',
        f'<title>{escape(SITE_NAME)}</title>',
        f'<link>{escape(site_url)}</link>',
        f'<description>{escape(SITE_DESCRIPTION)}</description>',
    ]

    for item in items:
        article_url = absolute_url(request, 'news_detail', item.id)
        xml_parts.extend([
            '<item>',
            f'<title>{escape(item.title or SITE_NAME)}</title>',
            f'<link>{escape(article_url)}</link>',
            f'<guid>{escape(article_url)}</guid>',
            f'<description>{escape(clean_description(item.text, 240))}</description>',
            f'<pubDate>{item.created_at.strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>' if item.created_at else '',
            '</item>',
        ])

    xml_parts.extend(['</channel>', '</rss>'])

    return HttpResponse('\n'.join(part for part in xml_parts if part), content_type='application/rss+xml')
