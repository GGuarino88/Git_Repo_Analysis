from django.contrib import admin

from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("index/",views.index, name="index"),
    path("analyze",views.analyze,name="analyze"),
]