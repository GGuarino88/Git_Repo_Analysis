from django.shortcuts import render

# Create your views here.

def home(request):
    context={}
    return render(request, "RepoAnalysisApp/home.html", context)

def index(request):
    context={}
    return render(request, "RepoAnalysisApp/index.html", context)

def results(request):
    context={}
    return render(request, "RepoAnalysisApp/resuts.html", context)