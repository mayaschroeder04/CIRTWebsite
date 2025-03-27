import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.db.models import Q
from .models import Document
from .forms import CustomUserCreationForm


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


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Login Success")
            return redirect("homepage")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print(
                f"User created with username: {form.cleaned_data.get('username')} and password: {form.cleaned_data.get('password1')} and email: {form.cleaned_data.get('email')}"
            )
            return redirect("login")
        else:
            print("Form errors:", form.errors)
            return render(
                request, "register.html", {"form": form, "error": "not working"}
            )
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


# def contact_view(request):
#     return render(request, "contact-us.html")
#


def search_results(request):
    query = request.GET.get("query", None)
    filter_category = request.GET.get("filter", None)
    documents = Document.objects.select_related("category").all()

    if query:
        documents = documents.filter(
            Q(title__contains=query)
            | Q(description__contains=query)
            | Q(author__contains=query)
        )

    if filter_category and filter_category != "All":
        documents = documents.filter(category__id=filter_category)

    documents_data = [
        {
            "id": doc.id,
            "title": doc.title,
            "description": doc.description,
            "author": doc.author,
            "category_id": (
                doc.category.id if doc.category else None
            ),  # Avoid null reference error
            "category_name": (
                doc.category.name if doc.category else "Unknown"
            ),  # Fetch category name
        }
        for doc in documents
    ]

    documents_json = json.dumps(documents_data)

    # Debugging
    print("Documents JSON:", documents_json)

    return render(
        request,
        "search-results.html",
        {"documents_json": documents_json, "filter": filter_category, "qry": query},
    )
