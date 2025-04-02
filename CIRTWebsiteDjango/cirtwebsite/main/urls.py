from django.urls import path
from . import views

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
    path("check-status/", views.check_status, name="check_status"),
    path("button-two", views.button_two, name="button_two"),
    path("button-four", views.button_four, name="button_four"),
    path("awaiting-review/", views.awaiting_review, name="awaiting_review"),
    path("forgot-username/", views.forgot_username, name="forgot_username"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("sign-up/", views.sign_up, name="sign_up"),

    path("terms-and-conditions/", views.terms_conditions, name="terms_conditions"),

    path("upload-journal/", views.upload_journal, name="upload_journal"),
]
