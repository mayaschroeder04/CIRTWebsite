from django.urls import path, include
from . import views, admin





urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("fake_journal/", views.fake_journal, name="fake_journal"),
    path("terms-and-conditions/", views.toc, name="terms-and-conditions"),
    path("journals/", views.journals_view, name="journals"),
    # path("contact-us/", views.contact, name="contact-us"), #  Need a contact us
    path("images/", views.images_view, name="images"),
    path("authors/", views.authors_view, name="authors"),
    # path("about-us/", views.about_us, name="about-us"),  #  Need to create an about us page
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),  #  Need to be created
    # path("register/", views.register_view, name="register"),
    # path("upload/", views.upload_view, name="upload"),
    path("pdfviewer/", views.pdf_view, name="pdfviewer"),
    path("search-results/", views.search_results, name="search_results"),
    path("search-results/", views.filter_buttons, name="filter_buttons"),
    path("upload-images/", views.upload_images, name="upload_images"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path("past-uploads/", views.past_uploads, name="past_uploads"),
    path("past-reviews/", views.past_reviews, name="past_reviews"),
    path("editor-dashboard/", views.editor_dashboard, name="editor_dashboard"),
    path('check_status/', views.check_status, name='check_status'),
    path("button-two", views.button_two, name="button_two"),
    path("button-four", views.button_four, name="button_four"),
    path("awaiting-review/", views.awaiting_review, name="awaiting_review"),
    path("forgot-username/", views.forgot_username, name="forgot_username"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("reviewer-dashboard/", views.reviewer_dashboard, name="reviewer_dashboard"),
    path("terms-and-conditions/", views.terms_conditions, name="terms_conditions"),
    path("view-uploads/", views.view_uploads, name="view_uploads"),
    path("upload-journal/", views.upload_journal, name="upload_a_journal"),
    path("assigned-journals/", views.assigned_journals, name="assigned_journals"),
    path('accounts/', include('allauth.urls')),
    path('view-uploads/', views.view_uploads, name="view_uploads"),

    path('verify_email/<uidb64>/<token>/', views.verify_email, name="verify_email"),

    path('login-otp/', views.login_otp, name="login_otp"),

    path('generate_presigned_url/<path:file_path>/', views.generate_presigned_url, name='generate_presigned_url'),

    path('set-password/', views.set_password, name="set_password"),

    path('autocomplete/', views.autocomplete, name='autocomplete'),

    path("privacy-policy/", views.privacy_policy_view, name="privacy-policy"),

    path("faq/", views.faq_view, name="faq"),

    path("terms-and-conditions/",views.terms_and_conditions_view,name="terms-and-conditions",),

    path("cookie-policy/", views.cookie_policy_view, name="cookie-policy"),

    path("contact/", views.contact_view, name="contact"),

    path('save-document/<path:documentId>/', views.save_user_documents, name="save_document"),

    path('unsave-document/<path:documentId>/', views.unsave_user_documents, name="unsave_document"),

    path('cite-document/<path:documentId>/', views.cite_document, name="cite-document"),

    path('download-document/<path:documentId>/', views.download_document, name="download_document"),

    path('view_pdf/<int:doc_id>/', views.view_pdf, name='view_pdf'),

    path('submit-review/<int:journal_id>/', views.submit_review, name='submit_review'),

    path('reviewed_journals/', views.reviewed_journals, name='reviewed_journals'),
    
    path('flagged_revision/', views.flagged_revision, name='flagged_revision'),

    path('saved-journals/', views.saved_journals, name='saved_journals'),

    path('review-status/', views.review_status, name='review_status'),

    path('user-profile/', views.user_profile, name='user_profile')
]
