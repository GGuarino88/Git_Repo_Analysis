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
    path('index/scan-create/', views.scan_create, name='scan-create'),
    path('index/scan-edit/<int:pk>', views.scan_edit, name='scan-edit'),
    path('index/scan-delete/<int:pk>', views.scan_delete, name='scan-delete'),
    path('index/<str:scan_session>/repo-create/', views.repo_create, name='repo-create'),
    path('index/<str:scan_session>/repo-edit/<int:pk>', views.repo_edit, name='repo-edit'),
    path('index/<str:scan_session>/repo-delete/<int:pk>', views.repo_delete, name='repo-delete'),
    path('index/<str:scan_session>', views.scan, name='scan'),
    path('index/<str:scan_session>/<str:url_name>/analyze',views.analyze,name='analyze'),
    path('about', views.about, name='about'),
]
