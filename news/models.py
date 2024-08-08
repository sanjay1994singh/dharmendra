from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'category'


# class Author(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)
#     desc = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
#
#     def __str__(self):
#         return str(self.name)
#
#     class Meta:
#         db_table = 'category'


class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='news_image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'news'


class OtherNewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True, blank=True)
    other_image = models.ImageField(upload_to='other_news_image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.news.title)

    class Meta:
        db_table = 'other_news_image'
