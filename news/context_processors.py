# context_processors.py

from .models import Category


def categories_processor(request):

    categories = Category.objects.all().order_by('name')

    return {
        'categories': categories
    }
