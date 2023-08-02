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
    path('index/semester-create/', views.semester_create, name='semester-create'),
    path('index/semester-edit/<int:pk>', views.semester_edit, name='semester-edit'),
    path('index/semester-delete/<int:pk>', views.semester_delete, name='semester-delete'),
    path('index/<str:semester>/project-create/', views.project_create, name='project-create'),
    path('index/<str:semester>/project-edit/<int:pk>', views.project_edit, name='project-edit'),
    path('index/<str:semester>/project-delete/<int:pk>', views.project_delete, name='project-delete'),
    path('index/<str:semester>', views.scan, name='scan'),
    path('index/<str:semester>/<str:url_name>/analyze',views.analyze,name='analyze'),
    path('scan/<str:semester>/generate-all-reports/', views.generate_all_reports, name='generate-all-reports'),
    path('about', views.about, name='about'),
]