from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, UserForm, UserProfileForm, PageForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def visitor_cookie_handler(request):
    visits = int(request.session.get('visits', '1'))

    last_visit_cookie = request.session.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def index(request):
    visitor_cookie_handler(request)

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list


    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    visits = request.session.get('visits', 1)

    context_dict = {'visits': visits}

    return render(request, 'rango/about.html', context=context_dict)

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

@login_required
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

@login_required
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

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # 1. Save User form data
            user = user_form.save()
            # 2. Hash encryption of the password
            user.set_password(user.password)
            user.save()

            # 3. Save Profile form data
            profile = profile_form.save(commit=False)
            # 4. Set the Profile to the User you just created
            profile.user = user

            # 5. Process uploaded images
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # 6. Finally save the profile
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    # If it's a POST request, it means the user submitted a form
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to authenticate user
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        # If it's a GET request, display the login page.
        return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')