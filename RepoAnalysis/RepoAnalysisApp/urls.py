from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from allauth.socialaccount.providers.github import views as github_view
urlpatterns = [    
    # admin view url
    path('admin/', admin.site.urls, name='admin'),
    
    # allauth views url
    path('accounts/', include('allauth.urls')),
    
    # custom view url
    path('login/', views.repoAnalysisLogin, name='login'),
    path('logout/', views.repoAnalysisLogout, name='logout'),
    
    # application views url
    path('', views.home, name='home'),
    path('index/',views.index, name='index'),
    path('index/<str:scan_session>', views.scan, name='scan'),
    path('index/<str:scan_session>/analyze',views.analyze,name='analyze'),
    path('about', views.about, name='about'),
]