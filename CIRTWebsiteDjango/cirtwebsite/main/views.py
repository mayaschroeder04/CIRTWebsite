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
    query = request.GET.get("query", None  )
    filter_category = request.GET.get("filter", None )
    documents = Document.objects.select_related('category').all()

    if query:
        documents = documents.filter(
            Q(title__contains=query) |
            Q(description__contains=query) |
            Q(author__contains=query))

    if filter_category and filter_category != "All":
        documents = documents.filter(category__id=filter_category)

    documents_data = [
        {
            "id": doc.id,
            "title": doc.title,
            "description": doc.description,
            "author": doc.author,
            "category_id": doc.category.id if doc.category else None,  # Avoid null reference error
            "category_name": doc.category.name if doc.category else "Unknown"  # Fetch category name
        }
        for doc in documents
    ]

    documents_json = json.dumps(documents_data)

    # Debugging
    print("Documents JSON:", documents_json)

    return render(request, "search-results.html", {
        "documents_json": documents_json,
        "filter": filter_category,
        "qry": query
    })