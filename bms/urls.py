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

urlpatterns = [
    # path('', views.home, name='home'),
    # path('home/', views.home, name='home'),
    path('books/', views.BooksView.as_view(), name='books'),
    path('book/', views.BookView.as_view(), name='books'),
    path('book/<int:pk>', views.BookView.as_view(), name='book'),
    re_path(r'^media/uploads/(?P<pk>\w+)/books/*', views.BookView.as_view(), name='book'),
    re_path(r'^media/uploads/(?P<pk>\w+)/book-covers/*', views.BookView.as_view(), name='book'),
    #re_path(r'media/(?P<path>.*)$'

   
    ]