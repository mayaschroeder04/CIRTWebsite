from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("fake_journal/", views.fake_journal, name="fake_journal"),
    path("terms-and-conditions/", views.TOC, name="terms-and-conditions"),
]
