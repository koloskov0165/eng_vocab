"""proj_eng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('vocab', views.vocab),
    path('add_word', views.add_word),
    path('send_word', views.send_word),
    path('start_test', views.start_test),
    path('test', views.test),
    path('send_answer', views.send_answer),
    path('test_result', views.test_result),
    path('finish_test', views.finish_test),
]
