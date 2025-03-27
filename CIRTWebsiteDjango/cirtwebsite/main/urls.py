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
    path("pdfviewer/", views.pdf_view, name="pdfviewer"),
    path("search-results/", views.search_results, name="search_results"),
]
