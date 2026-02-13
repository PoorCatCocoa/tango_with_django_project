from django.contrib import admin
from django.urls import path
from django.urls import include  # <--- Must import include
from django.conf import settings
from django.conf.urls.static import static
from rango import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rango/', include('rango.urls')), # Map the root path to rango
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)