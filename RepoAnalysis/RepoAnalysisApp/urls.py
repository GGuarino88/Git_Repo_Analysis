from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from allauth.socialaccount.providers.github import views as github_view
from . import views

urlpatterns = [    
    # admin view url
    path('admin/', admin.site.urls),
    
    # allauth views url
    path('accounts/', include('allauth.urls')),
    
    # custom view url
    path('login/', views.repoAnalysisLogin, name='login'),
    path('logout/', views.repoAnalysisLogout, name='logout'),
    
    # application views url
    path('', views.home, name='home'),
    path('index/',views.index, name='index'),
    path('analyze',views.analyze,name='analyze'),
    path('about', views.about, name='about'),
]