from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    return render(request, 'main.html')
# Create your views here.
def homepage(request):
    return render(request, "homepage.html")

 
def fake_journal(request):
    return render(request, "fake_journal-2.html")


def TOC(request):
    return render(request, "terms-and-conditions.html")
