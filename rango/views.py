from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    # 1. Query the database: Retrieve the top 5 categories by number of likes
    category_list = Category.objects.order_by('-likes')[:5]

    # 2. Building a dictionary: putting the query results into context_dict
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    # 3. Rendering template
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    # Create a context dictionary
    context_dict = {}

    try:
        # 1. Try to find the corresponding category based on slug.
        category = Category.objects.get(slug=category_name_slug)

        # 2. If found, retrieve all pages belonging to this category.
        pages = Page.objects.filter(category=category)

        # 3. Put this data into a dictionary
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        # 4. If not found, set the category to None.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Rendering template
    return render(request, 'rango/category.html', context=context_dict)