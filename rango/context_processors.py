from rango.models import Category

def visits(request):
    return {'visits': request.session.get('visits', 1)}