from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("home/settings", views.user_settings, name="user_settings"),
    path("home/settings/change_password", views.change_password, name="change_password"),
    path("home/settings/change_club", views.change_club, name="change_club"),
    path("home/settings/change_favorite", views.change_favorite, name="change_favorite"),
    path("home/new_belt", views.new_belt, name="new_belt"),
    path("home/new_victory", views.new_victory, name="new_victory"),
    path("home/new_medal", views.new_medal, name="new_medal"),
    path("", include("drills.urls")),
    path("", include("badges.urls")),
]