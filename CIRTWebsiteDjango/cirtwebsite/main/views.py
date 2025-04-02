import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .models import Category, Document, SubCategory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import UserManager, User

# from ..mysql.connector.utils import print_buffer


# from React import catch


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

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("homepage")
    return redirect("homepage")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Username:", username)
        print("Password:", password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid username or password.")
            return JsonResponse({"message": "Invalid username or password."})

    return render(request, "login_view.html")

# def contact_view(request):
#     return render(request, "contact-us.html")

def filter_buttons(request):
        categories = Category.objects.all()

        # Fetch the subcategories for each category (related to the category model)
        # 'subcategories' is the related name in the SubCategory model
        # print("test")
        # print("Categories:", categories)
        # for category in categories:
        #     print_buffer(f"Category: {category.name}, Subcategories: {[sub.name for sub in category.subcategories.all()]}")

        return render(request, "search-results.html", {
            "categories": categories
        })



def homepage(request):
    documents = Document.objects.select_related('category').order_by('-created_at')[:3]
    categories = Category.objects.all()

    category_data = [
        {"id": cat.id, "name": cat.name} for cat in categories
    ]


    documents_json = json.dumps([
        {"title": doc.title,
         "author": doc.author,
         "description": doc.description,
         "category_name": doc.category.name,
         "file_url": doc.file_url,
         }
        for doc in documents
    ])

    return render(request, "homepage.html", {"documents_json": documents_json, "categories": category_data})


def search_results(request):
    query = request.GET.get("query", None  )
    filter_category = request.GET.get("filter", None )
    documents = Document.objects.select_related('category').all()
    cat = Category.objects.all()
    print("Category:", cat )


    category_name = "All Categories"

    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__icontains=query))

    if filter_category and filter_category != "All":
        documents = documents.filter(category__id=filter_category)
        category = Category.objects.get(id=filter_category)
        categories = Category.objects.all()

    documents_data = [
        {
            "id": doc.id,
            "title": doc.title,
            "description": doc.description,
            "file_url": doc.file_url,
            "author": doc.author,
            "category_id": doc.category.id if doc.category else None,  # Avoid null reference error
            "category_name": doc.category.name if doc.category else "Unknown"  # Fetch category name
        }
        for doc in documents
    ]

    documents_json = json.dumps(documents_data)

    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()

    # category_json = json.dumps([
    #     {"id": cat.id, "name": cat.name} for cat in categories
    # ])
    #
    # sub_category_json = json.dumps([
    #     {"id": sub_cat.id, "name": sub_cat.name} for sub_cat in sub_categories
    # ])

    # Debugging
    # print("Documents JSON:", documents_json)

    return render(request, "search-results.html", {
        "documents_json": documents_json,
        "filter": filter_category,
        "qry": query,
        "category_name": category_name,
        "categories": categories,
    })


def upload_images(request):
    return render(request, "upload-images.html")

def student_dashboard(request):
    return render(request, "student-dashboard.html")

def past_uploads(request):
    return render(request, "past-uploads.html")

def past_reviews(request):
    return render(request, "past-reviews.html")

def editor_dashboard(request):
    return render(request, "editor-dashboard.html")

def check_status(request):
    return render(request, "check-status.html")

def button_two(request):
    return render(request, "button-two.html")

def button_four(request):
    return render(request, "button-four.html")

def awaiting_review(request):
    return render(request, "awaiting-review.html")

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            return JsonReponse({'success': False, "message": "Passwords must match."})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, "message": "Username already exists."})

        User.objects.create_user(username, email, password)
        return JsonResponse({'success': True})

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': True, "message": "Instructions sent"})
        else:
            return JsonResponse({'success': False, "message": "Email doesn't exist"})
def forgot_username(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': True,
                'message': 'If an account exists with this email, you will receive instructions shortly.',
                'html': '<div class="success-message">If an account exists with this email, you will receive instructions shortly.</div>'
            })
        else:
            return JsonResponse({
                'success': True,
                'message': 'Instructions sent'
            })