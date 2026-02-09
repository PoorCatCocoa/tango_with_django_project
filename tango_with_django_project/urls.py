from django.contrib import admin
from django.urls import path
from django.urls import include  # <--- Must import include

urlpatterns = [
    path('rango/', include('rango.urls')), # Map the root path to rango
    path('admin/', admin.site.urls),
]