from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("create_club/", views.create_club_page, name="create_club_page"),
    path("create_user/", views.create_account_page, name="create_account_page"),
    path("create_club/submit/", views.create_a_club, name="create_a_club"),
    path("create_user/submit/", views.create_an_user, name="create_an_user"),
    path("login/submit/", views.account_login, name="account_login"),
]