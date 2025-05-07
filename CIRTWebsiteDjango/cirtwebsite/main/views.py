import json
import random
import string
import time
import boto3
from django.core.cache import cache
from datetime import timedelta
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .models import Category, Document, Subcategory
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from botocore.exceptions import NoCredentialsError, ClientError


# Use your custom user model throughout
CustomerUser = get_user_model()

# ---------------------------
# Basic Page Views
# ---------------------------
def homepage(request):
    saved_document_ids = []  # Default to empty list

    if(request.user.is_authenticated):
        print("hererer")
        user = CustomerUser.objects.get(id=request.user.id)
        print(user.username)
        saved_documents = user.saved_documents.all()
        print("SAVED: ", saved_documents)
        saved_document_ids = list(user.saved_documents.values_list('id', flat=True))
        print(saved_document_ids)

    documents = Document.objects.select_related('category').order_by('-created_at')[:3]
    categories = Category.objects.all()
    category_data = [{"id": cat.id, "name": cat.name} for cat in categories]
    documents_json = json.dumps([
        {"id": doc.id,
         "title": doc.title,
         "author": doc.author,
         "description": doc.description,
         "category_name": doc.category.name,
         "file_url": doc.file_url}
        for doc in documents
    ])
    return render(request, "homepage.html", {"documents_json": documents_json, "categories": category_data, "saved_documents": saved_document_ids})


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


def filter_buttons(request):
    categories = Category.objects.all()
    return render(request, "search-results.html", {"categories": categories})

def past_uploads(request):
    if request.method == "POST":
        user = request.user
        documents = Document.objects.filter(submitted_user=user.id)
        data = [
            {
                "id": doc.id,
                "title": doc.title,
                "description": doc.description,
                "file_url": doc.file_url,
                "author": doc.author,
                "category_id": doc.category.id if doc.category else None,
                "category_name": doc.category.name if doc.category else "Unknown"
            }
            for doc in documents
        ]
        return JsonResponse(data, safe=False)

def view_uploads(request):
    uploads = Document.objects.all()


    return render(request, 'view-uploads.html', {
        'uploads': uploads
    })

def assigned_journals(request):
    journals = Document.objects.all()  # no filter
    return render(request, 'assigned-journals.html', {
        'pending_journals': journals
    })

def past_reviews(request):
    return render(request, "past-reviews.html")


def editor_dashboard(request):
    return render(request, "editor-dashboard.html")

def check_status(request):
    user = request.user
    documents = Document.objects.filter(submitted_user=user.id)
    return render(request, 'check-status.html', {'documents': documents})

# ---------------------------
# Document & Search Views
# ---------------------------
def search_results(request):
    query = request.GET.get("query", None)
    filter_category = request.GET.get("filter", None)
    documents = Document.objects.select_related('category').all()
    cat = Category.objects.all()
    print("Category:", cat)
    category_name = "All Categories"

    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__icontains=query)
        )

    if filter_category and filter_category != "All":
        documents = documents.filter(category__id=filter_category)

    categories = Category.objects.all()
    sub_categories = Subcategory.objects.all()

    if request.method == 'POST':
        data = json.loads(request.body)
        selected_categories = data.get('selected_categories', [])
        selected_subcategories = data.get('selected_subcategories', [])
        print('Selected Categories:', selected_categories)
        print('Selected Subcategories:', selected_subcategories)

        documents = Document.objects.all()
        if selected_categories:
            documents = documents.filter(category__id__in=selected_categories)
        # Uncomment and update if you want to filter by subcategories:
        # if selected_subcategories:
        #     documents = documents.filter(subcategory_id__in=selected_subcategories)

        documents_filtered = list(documents.values(
            "id", "title", "description", "file_url", "author",
            "category__id", "category__name"
        ))
        print(type(documents_filtered))
        print(documents_filtered)
        return JsonResponse({'documents': documents_filtered}, safe=False)

    documents_data = [
        {
            "id": doc.id,
            "title": doc.title,
            "description": doc.description,
            "file_url": doc.file_url,
            "author": doc.author,
            "category_id": doc.category.id if doc.category else None,
            "category_name": doc.category.name if doc.category else "Unknown"
        }
        for doc in documents
    ]
    documents_json = json.dumps(documents_data)
    return render(request, "search-results.html", {
        "documents_json": documents_json,
        "filter": filter_category,
        "qry": query,
        "category_name": category_name,
        "categories": categories,
        "sub_categories": sub_categories,
    })


def upload_images(request):
    return render(request, "upload-images.html")


def student_dashboard(request):
    return render(request, "student-dashboard.html")

def reviewer_dashboard(request):
    return render(request, "reviewer-dashboard.html")

# def view_uploads(request):
#     journals = Document.objects.all()
#     return render(request, 'view-uploads.html', {'pending_journals': journals})

def assigned_journals(request):
    journals = Document.objects.all()  # no filter
    return render(request, 'assigned-journals.html', {
        'pending_journals': journals
    })



def past_reviews(request):
    return render(request, "past-reviews.html")


def editor_dashboard(request):
    return render(request, "editor-dashboard.html")


def check_status(request):
    user = request.user
    documents = Document.objects.filter(submitted_user=user.id)
    return render(request, 'check-status.html', {'documents': documents})



def button_two(request):
    return render(request, "button-two.html")


def button_four(request):
    return render(request, "button-four.html")


def awaiting_review(request):
    return render(request, "awaiting-review.html")


# ---------------------------
# Authentication & Account Views
# ---------------------------
def send_verification_email(user, request):
    print("hrere")
    print(user)
    token = default_token_generator.make_token(user)
    print("token", token)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    print(f"User ID: {user.pk}, Token: {token}, Encoded UID: {uid}")
    verification_url = urljoin(request.build_absolute_uri('/verify_email/'), f"{uid}/{token}/")
    print("URL: ", verification_url)
    subject = "Verify your email address"
    message = render_to_string("email/verification_email.html", {"verification_url": verification_url})
    send_mail(subject, message, "from@example.com", [user.email])


def verify_email(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = CustomerUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomerUser.DoesNotExist):
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
        if password != confirm_password:
            return JsonResponse({'success': False, "message": "Passwords must match."}, status=400)
        if CustomerUser.objects.filter(email=email).exists():
            return JsonResponse({'success': False, "message": "Email is already in use."}, status=409)
        if CustomerUser.objects.filter(username=username).exists():
            return JsonResponse({'success': False, "message": "Username already exists."}, status=409)
        try:
            user = CustomerUser.objects.create_user(username=username, email=email, password=password, is_active=False)
            send_verification_email(user, request)
            return JsonResponse({'success': True, 'message': 'User created successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Error: {str(e)}"}, status=500)


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print("CSRF Token Received:", request.META.get("HTTP_X_CSRFTOKEN"))
        if CustomerUser.objects.filter(email=email).exists():
            user = CustomerUser.objects.get(email=email)
            send_reset_password_email(user, request)
            return JsonResponse({'success': True, "message": "Instructions sent"})
        return JsonResponse({'success': False, "message": "Email doesn't exist"})
    return JsonResponse({'success': False, "message": "Invalid request."})


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
        user = CustomerUser.objects.get(pk=uid)
    except (CustomerUser.DoesNotExist, ValueError, TypeError, OverflowError):
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
        user = CustomerUser.objects.filter(email=email).first()
        if user:
            send_mail(
                'Your Username',
                f'Your username is: {user.username}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({
                'success': True,
                'message': 'If an account exists with this email, you will receive instructions shortly.'
            })
        else:
            return JsonResponse({'success': False, 'message': "Email not found."})
    return JsonResponse({'success': False, 'message': "Invalid request."})


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
                request.session['otp_user'] = user.username
                return JsonResponse({"success": True, "redirect_url": "verify_otp?username=" + username})
            else:
                login(request, user)
                return JsonResponse({"success": True, "message": "Logging in...", "redirect_url": "/"})
        else:
            return JsonResponse({"success": False, "message": "Invalid username or password."})
    return render(request, "login_view.html")


def generate_otp_for_user(user):
    otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    cache.set(f"otp_{user.username}", otp, timeout=300)
    return otp


def send_otp_email(email, otp):
    message = f"Your OTP is: {otp}"
    header = "One time password"
    send_mail(header, message, "from@example.com", [email])


def login_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        username = request.POST.get("username")
        user = CustomerUser.objects.get(username=username)
        if verify_otp_user(user, otp):
            print("made it here!")
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return JsonResponse({"success": True, "message": "Logging in...", "redirect_url": "/"})
        else:
            return JsonResponse({"success": False, "message": "Invalid OTP.", "redirect_url": "#login_otp?username=" + user.username})
    return render(request, "login_view.html")


def verify_otp_user(user, otp):
    print(cache.get(f"otp_{user.username}"))
    print(otp)
    for _ in range(5):  # Retry 5 times max
        otp_cached = cache.get(f"otp:{user.username}")
        if otp_cached:
            break
        time.sleep(0.1)
    cached_otp = cache.get(f"otp_{user.username}")
    return cached_otp == otp


def terms_conditions(request):
    return render(request, "terms_and_conditions.html")


# ---------------------------
# Document Upload & Viewing
# ---------------------------
def upload_journal(request):
    if request.method == "POST":

        type = request.POST.get("type")
        user_id = request.POST.get("user_id")
        file = request.FILES.get("journal")
        title = request.POST.get("title")
        author = request.POST.get("author")
        category = request.POST.get("category")
        description = request.POST.get("description")
        subcategory = request.POST.get("subcategory")
        subcategory_instance = Subcategory.objects.get(name=subcategory)

        if not title:
            return JsonResponse({"status": "error", "message": "Missing title"})
        if not file:
            return JsonResponse({"status": "error", "message": "Missing file"})
        if file.content_type != "application/pdf":
            return JsonResponse({"status": "error", "message": "Only PDF files are allowed"})
        if type == 'journal':
            upload_document(file, title, description, author, category, user_id, type, subcategory_instance)
        elif type == 'image':
            pass
        else:
            return JsonResponse({"status": "error", "message": "Invalid type"})
        return JsonResponse({"status": "success", "message": "Upload successful!"})
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    return render(request, "upload_a_journal.html", {'categories': categories, 'subcategories': subcategories})


# def upload_image(file, title, description, author, user_id ):
#     s3_client = boto3.client('s3',
#                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#                              region_name=settings.AWS_S3_REGION_NAME)
#     file_path = f"{type}"


def upload_document(file, title, description, author, category, user_id, type, subcategory):
    s3_client = boto3.client('s3',
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                             region_name=settings.AWS_S3_REGION_NAME)
    category_instance = Category.objects.get(name=category)
    file_path = f"{type}/{category.replace(' ', '-')}/{title.replace(' ', '-')}.pdf"
    s3_client.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_path,
                             ExtraArgs={
                                 "ContentType": file.content_type,
                                 "ContentDisposition": "inline"
                             })
    document = Document.objects.create(
        title=title,
        description=description,
        category=category_instance,
        file_url=file_path,
        author=author,
        submitted_user=user_id,
        file_size=file.size,
        subcategory = subcategory
    )
    return document


def view_document(request, document_id):
    document = Document.objects.get(id=document_id)
    file_path = document.file_url.split(f"{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/")[1]
    presigned_url = document.presigned_url(file_path)
    print("presigned url: ", presigned_url)
    print("filepath: ", file_path)
    if presigned_url:
        return redirect(presigned_url)
    else:
        return HttpResponse("unable to fetch presigned url")


def generate_presigned_url(request, file_path):
    print(file_path)
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME)
    print("here")
    try:
        url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                       'Key': file_path},
                                               ExpiresIn=3600)
        return JsonResponse({"url": url})
    except ClientError as e:
        return JsonResponse({'error': str(e)}, status=500)


def journals_view(request):
    # Get all documents (which you might be using as journals)
    journals = Document.objects.all().order_by("title")  # Use Document instead of Journal
    
    # Pass journals as a context variable to the template
    return render(request, 'journals.html', {'journals': journals})


def autocomplete(request):
    query = request.GET.get("query", "")
    documents = Document.objects.select_related("category").filter(
        Q(title__istartswith=query)
    )[:10]  # Limit suggestions for performance
    #Q(title__icontains=query) |
    #Q(description__icontains=query) |
    #Q(author__icontains=query)
    suggestions = [doc.title for doc in documents]
    return JsonResponse(suggestions, safe=False)

    # Debugging
    print("Documents JSON:", documents_json)

    return render(
        request,
        {"documents_json": documents_json},
    )

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



def save_user_documents(request, documentId):
    if request.method == "POST":
        if (request.user.is_authenticated):
            # document_id = request.POST.get("document_id")
            print(request.user.id)
            user_id = request.user.id
            user = CustomerUser.objects.get(id=user_id)
            user.saved_documents.add(documentId)
            print("here")
            print(user.saved_documents.all())
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "message": "Make an account to save!"})
    else:
        return JsonResponse({"success": False})

def unsave_user_documents(request, documentId):
    if request.method == "POST":
        if (request.user.is_authenticated):
            # document_id = request.POST.get("document_id")
            print(request.user.id)
            user_id = request.user.id
            user = CustomerUser.objects.get(id=user_id)
            user.saved_documents.remove(documentId)
            print(user.saved_documents.all())
            return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

def display_user_documents(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = CustomerUser.objects.get(id=user_id)
        documents = user.saved_documents.all()

        categories = Category.objects.all()

        category_data = [{"id": cat.id, "name": cat.name} for cat in categories]

        documents_json = json.dumps([
            {"title": doc.title,
             "author": doc.author,
             "description": doc.description,
             "category_name": doc.category.name,
             "file_url": doc.file_url}
            for doc in documents
        ])

        return JsonResponse({"status": "success", "documents": documents_json, "categories": category_data})


def cite_document(request, documentId):
    if request.method == "POST":
            document = Document.objects.get(id=documentId)

            citation = document.get_citation()
            return JsonResponse({
                'success': True,
                'citation': citation  # Send the citation to the frontend
            })

    else:
        return JsonResponse({
            'success': False,
            'message': "Invalid request method."
        })

def download_document(request, documentId):
    if request.method == "POST":
        print(documentId)
        document = Document.objects.get(id=documentId)

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME)

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': document.file_url,
                'ResponseContentDisposition': f'attachment; filename="{document.title}.pdf"',
                'ResponseContentType': 'application/pdf'
            },
            ExpiresIn=3600
        )
        return JsonResponse({"success": True, "url": url})

    return JsonResponse({"success": True, 'url': url})

def view_pdf(request, doc_id):
    document = Document.objects.get(id=doc_id)
    file_path = document.file_url  # should be like 'Case-Studies/dfks.pdf'

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': file_path},
            ExpiresIn=3600
        )
    except ClientError as e:
        return HttpResponse(f"Error generating presigned URL: {str(e)}")

    return render(request, 'view_pdf.html', {
        'journal': document,
        'pdf_url': presigned_url
    })

def submit_review(request, journal_id):
    if request.method == "POST":
        journal = get_object_or_404(Document, id=journal_id)
        comment = request.POST.get("review_comment")

        # Save comment logic goes here (maybe to a Review model?)
        print(f"Review submitted for {journal.title}: {comment}")

        return redirect("assigned_journals")  # Or wherever you want to redirect

def reviewed_journals(request):
    return render(request, 'reviewed_journals.html')

def flagged_revision(request):
    return render(request, "flagged_revision.html")

def saved_journals(request):
    documents = request.user.saved_documents.all()
    categories = Category.objects.all()
    data = [
        {
            "id": doc.id,
            "title": doc.title,
            "description": doc.description,
            "file_url": doc.file_url,
            "author": doc.author,
            "category_id": doc.category.id if doc.category else None,
            "category_name": doc.category.name if doc.category else "Unknown"
        }
        for doc in documents
    ]
    return JsonResponse(data, safe=False)

def review_status(request):
    if request.method == "POST":
        user = request.user
        documents = Document.objects.filter(submitted_user=user.id)

        data = [
            {
                "id": doc.id,
                "title": doc.title,
                "description": doc.description,
                "file_url": doc.file_url,
                "author": doc.author,
                "category_id": doc.category.id if doc.category else None,
                "category_name": doc.category.name if doc.category else "Unknown",
                "status": doc.status
            }
            for doc in documents
        ]
        return JsonResponse({"success": True, "data": data})

def user_profile(request):
    if request.method == "POST":
        user = request.user

        return JsonResponse({"name": user.first_name + " " + user.last_name, "role": user.role, "email": user.email })
