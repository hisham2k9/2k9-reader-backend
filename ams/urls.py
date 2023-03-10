"""ams URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include,re_path
from . import views

# urlpatterns = [
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),
   
#     ]

    
urlpatterns = [
    path("redirect-to-front/", views.redirect_to_front, name = 'redirect-to-front'),
    path("csrf/", views.get_csrf, name="api-csrf"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path("whoami/", views.WhoAmIView.as_view(), name="whoami"),
]