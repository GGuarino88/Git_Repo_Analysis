from django.contrib import admin

from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home),
    path("index/",views.index),
    path("results/", views.results),
]