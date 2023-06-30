from django.contrib import admin

from django.urls import path, include
from django.contrib.auth import views as auth_views
from allauth.socialaccount.providers.github import views as github_view

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login/', github_view.oauth2_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('index/',views.index, name='index'),
    path('analyze',views.analyze,name='analyze'),
]