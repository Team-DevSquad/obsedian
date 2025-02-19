from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('authenticate.urls')),
    path('api/',include('api.urls')),
    path('blog/',include('blog.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('portal/',include('portal.urls')),
    path('',views.home)
]
