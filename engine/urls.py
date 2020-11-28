
from django.contrib import admin
from django.urls import path
from django.urls import include

from .views import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hostel.urls')),
]
