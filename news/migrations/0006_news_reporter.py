# Generated by Django 5.1.1 on 2024-09-06 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_news_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='reporter',
            field=models.CharField(default='Dharmendra Chaturvedi', max_length=100),
        ),
    ]
