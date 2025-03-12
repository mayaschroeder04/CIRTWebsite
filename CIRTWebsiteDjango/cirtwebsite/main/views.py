from django.shortcuts import render


# Create your views here.
def homepage(request):
    return render(request, "homepage.html")


def fake_journal(request):
    return render(request, "fake_journal-2.html")



def TOC(request):
    return render(request, "terms-and-conditions.html")

def journals_view(request):
    return render(request, "journals.html")

def images_view(request):
    return render(request, "images.html")

def authors_view(request):
    return render(request, "authors.html")

def pdf_view(request):
    return render(request, "pdfviewer.html")

def search_results(request):
    return render(request, "search-results.html")