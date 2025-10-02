from django.urls import path

from . import views

urlpatterns = [
    path("home/badges/", views.badges_page, name="badges_page"),
]