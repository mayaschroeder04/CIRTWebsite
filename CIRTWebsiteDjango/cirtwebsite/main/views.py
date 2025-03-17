import json
from django.shortcuts import render
from django.db.models import Q
from .models import Document

# Create your views here.
def homepage(request):
    return render(request, "homepage.html")


def fake_journal(request):
    return render(request, "fake_journal-2.html")



def toc(request):
    return render(request, "terms-and-conditions.html")

def journals_view(request):
    return render(request, "journals.html")

def images_view(request):
    return render(request, "images.html")

def authors_view(request):
    return render(request, "authors.html")

def pdf_view(request):
    return render(request, "pdfviewer.html")

# def contact_view(request):
#     return render(request, "contact-us.html")
#

def search_results(request):
    qry = request.GET.get("query", None  )
    filter_category = request.GET.get("filter", None )
    documents = Document.objects.all()

    if qry:
        documents = documents.filter(
            Q(title__contains=qry) |
            Q(description__contains=qry) |
            Q(author__contains=qry))

    if filter_category:
        if filter_category and filter_category != "All":
            documents = documents.filter(category__iexact=filter_category)

    documents_json = json.dumps(list(documents.values("id", "title", "description", "author", "category_id")))

    return render(request, "search-results.html", {"documents": documents_json, "filter": filter, "qry": qry})

