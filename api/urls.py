"""
URL configuration for api project.
Email Address: sharathn.shet@walamrt.com
First Name: sharu
Last Name: shet
Birth day: 1996-09-15               
Password: 
Password (again):
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import authenticate ,login, logout ,views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('apiuser.urls')),
    path('socialapi/',include('social_apps.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
