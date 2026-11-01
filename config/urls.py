from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Point the root URL to the generator app's URLs
    path('', include('apps.generator.urls')), 
]