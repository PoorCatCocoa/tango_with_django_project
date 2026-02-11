from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse

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

def add_category(request):
    form = CategoryForm()

    # If it's a POST request, it means the user has submitted data.
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Check if the data is valid
        if form.is_valid():
            # Save to database
            form.save(commit=True)
            # After successful redirection, you will be redirected back to the homepage.
            return redirect('/rango/')
        else:
            print(form.errors)

    # If it's a GET request, or the data is invalid, display the form.
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # If the category does not exist, return None.
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                # Key step: Before saving, associate this page with the corresponding category.
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)