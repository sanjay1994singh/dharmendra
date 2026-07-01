from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('rss.xml', views.rss_feed, name='rss_feed'),
    path('news_detail/<int:id>/', views.news_detail, name='news_detail'),

    path('category/<int:id>/', views.category_news, name='category_news'),

    path('load-more/<int:id>/', views.load_more_news, name='load_more_news'),
]
