import json
import random
import string
import time
from django.core.cache import cache
from datetime import timedelta
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .models import Document
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Category, Document, SubCategory
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
    get_backends,
)
from django.contrib.auth.models import UserManager, User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from urllib.parse import urljoin, urlparse, parse_qs, urlencode

# from ..mysql.connector.utils import print_buffer
user = get_user_model()  #  For using auth in verifcication email

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

    return render(request, "search-results.html", {"categories": categories})


def homepage(request):
    documents = Document.objects.select_related("category").order_by("-created_at")[:3]
    categories = Category.objects.all()

    category_data = [{"id": cat.id, "name": cat.name} for cat in categories]

    documents_json = json.dumps(
        [
            {
                "title": doc.title,
                "author": doc.author,
                "description": doc.description,
                "category_name": doc.category.name,
                "file_url": doc.file_url,
            }
            for doc in documents
        ]
    )

    return render(
        request,
        "homepage.html",
        {"documents_json": documents_json, "categories": category_data},
    )


def search_results(request):
    query = request.GET.get("query", None)
    filter_category = request.GET.get("filter", None)
    documents = Document.objects.select_related("category").all()
    cat = Category.objects.all()

    category_name = "All Categories"

    if query:
        documents = documents.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(author__icontains=query)
        )

    if filter_category and filter_category != "All":
        documents = documents.filter(category__id=filter_category)

    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()

    if request.method == "POST":
        data = json.loads(request.body)

        selected_categories = data.get("selected_categories", [])
        selected_subcategories = data.get("selected_subcategories", [])

        # Filter documents first, then use `.values()`
        documents = Document.objects.all()

        if selected_categories:
            documents = documents.filter(category__id__in=selected_categories)
        # if selected_subcategories:
        #     documents = documents.filter(subcategory_id__in=selected_subcategories)

        # Convert to list of dictionaries
        documents_filtered = list(
            documents.values(
                "id",
                "title",
                "description",
                "file_url",
                "author",
                "category__id",
                "category__name",
            )
        )

        return JsonResponse({"documents": documents_filtered}, safe=False)

    documents_data = [
        {
            "id": doc.id,
            "title": doc.title,
            "description": doc.description,
            "file_url": doc.file_url,
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

    return render(
        request,
        "search-results.html",
        {
            "documents_json": documents_json,
            "filter": filter_category,
            "qry": query,
            "category_name": category_name,
            "categories": categories,
            "sub_categories": sub_categories,
        },
    )


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


def send_verification_email(user, request):
    print("hrere")
    print(user)
    token = default_token_generator.make_token(user)
    print("token", token)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    print(f"User ID: {user.pk}, Token: {token}, Encoded UID: {uid}")

    verification_url = urljoin(
        request.build_absolute_uri("/verify_email/"), f"{uid}/{token}/"
    )

    print("URL: ", verification_url)
    subject = "Verify your email address"
    message = render_to_string(
        "email/verification_email.html", {"verification_url": verification_url}
    )

    send_mail(subject, message, "from@example.com", [user.email])


def verify_email(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("email verified")
    else:
        return HttpResponse("email unverified")


def sign_up(request):
    if request.method == "POST":
        print("Made it here")

        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        confirm_password = request.POST.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            return JsonResponse(
                {"success": False, "message": "Passwords must match."}, status=400
            )

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"success": False, "message": "Email is already in use."}, status=409
            )

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"success": False, "message": "Username already exists."}, status=409
            )

        try:
            # Create user if no issues with email or username
            user = User.objects.create_user(
                username=username, email=email, password=password, is_active=False
            )

            send_verification_email(user, request)

            return JsonResponse(
                {"success": True, "message": "User created successfully!"}
            )
        except Exception as e:
            # Handle any unexpected errors
            return JsonResponse(
                {"success": False, "message": f"Error: {str(e)}"}, status=500
            )


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # Debug: Print the received CSRF token
        print("CSRF Token Received:", request.META.get("HTTP_X_CSRFTOKEN"))

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            send_reset_password_email(user, request)

            return JsonResponse({"success": True, "message": "Instructions sent"})

        return JsonResponse({"success": False, "message": "Email doesn't exist"})

    return JsonResponse({"success": False, "message": "Invalid request."})


def send_reset_password_email(user, request):
    print(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    query = urlencode({"uid": uid, "token": token})
    reset_url = f"{request.build_absolute_uri('/login/#set-password')}?{query}"

    subject = "Reset Your Password"
    message = f"Reset your password at {reset_url}"

    send_mail(subject, message, "from@example.com", [user.email])


def set_password(request):
    uid = request.POST.get("uid")
    token = request.POST.get("token")
    new_password = request.POST.get("password")

    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        return JsonResponse({"error": "Invalid link"}, status=400)

    if default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Token is invalid or expired"}, status=400)


def forgot_username(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            send_mail(
                "Your Username",
                f"Youre username is: {user.username}",
                "from@exmaple.com",
                [email],
                fail_silently=False,
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": "If an account exists with this email, you will receive instructions shortly.",
                }
            )
        else:
            return JsonResponse({"success": False, "message": "Email not found."})

    return JsonResponse({"success": False, "message": "Invalid request."})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username:", username)
        print("Password:", password)

        user = authenticate(request, username=username, password=password)

        otp_on_off = False
        if user is not None:

            if otp_on_off:
                otp = generate_otp_for_user(user)
                send_otp_email(user.email, otp)

                request.session["otp_user"] = user.username

                # Return a JSON response instead of redirecting immediately
                return JsonResponse(
                    {"success": True, "redirect_url": "verify_otp?username=" + username}
                )
            else:
                login(request, user)
                return JsonResponse(
                    {"success": True, "message": "Logging in...", "redirect_url": "/"}
                )

        else:
            return JsonResponse(
                {"success": False, "message": "Invalid username or password."}
            )

    return render(request, "login_view.html")


def generate_otp_for_user(user):
    otp = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    cache.set(f"otp_{user.username}", otp, timeout=300)

    return otp


def send_otp_email(email, otp):
    message = f"Your OTP is: {otp}"
    header = "One time password"

    send_mail(
        header,
        message,
        "from@example.com",
        [email],
    )


def login_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        username = request.POST.get("username")
        user = User.objects.get(username=username)

        if verify_otp_user(user, otp):
            print("made it here!")
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            if user.is_authenticated:
                print("logged in!")
                # return JsonResponse({"success": True})

            return JsonResponse(
                {"success": True, "message": "Logging in...", "redirect_url": "/"}
            )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid OTP.",
                    "redirect_url": "#login_otp?username=" + user.username,
                }
            )
    return render(request, "login_view.html")


def verify_otp_user(user, otp):
    print(cache.get(f"otp_{user.username}"))
    print(otp)
    for _ in range(5):  # Retry 5 times max
        otp_cached = cache.get(f"otp:{user.username}")
        if otp_cached:
            break
        time.sleep(0.1)  # 100ms delay

    cached_otp = cache.get(f"otp_{user.username}")
    return cached_otp == otp


def terms_conditions(request):
    # logic is here
    return render(request, "terms_and_conditions.html")


def privacy_policy_view(request):
    return render(request, "privacy-policy.html")


def faq_view(request):
    return render(request, "FAQ.html")


def terms_and_conditions_view(request):
    return render(request, "terms_and_conditions.html")


def cookie_policy_view(request):
    return render(request, "cookie-policy.html")


def contact_view(request):
    return render(request, "contact.html")


def upload_journal(request):
    if request.method == "POST":
        username = request.POST.get("username")

    return render(request, "upload_a_journal.html")

def autocomplete(request):

    query = request.GET.get("query", "")
    documents = Document.objects.select_related("category").filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(author__icontains=query)
    )[:10]  # Limit suggestions for performance

    suggestions = [doc.title for doc in documents]
    return JsonResponse(suggestions, safe=False)

    # Debugging
    print("Documents JSON:", documents_json)

    return render(
        request,
        {"documents_json": documents_json},
    )
