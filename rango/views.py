from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

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