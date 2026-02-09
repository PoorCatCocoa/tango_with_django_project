from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Build a dictionary and pass it to the template engine.
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    # Return to the rendered page
    # The first parameter is the request, the second is the template path, and the third is a dictionary.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')