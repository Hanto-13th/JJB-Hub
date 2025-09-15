from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


#the views to redirect to the page for login/create_club/create_user
def index(request):
    return render(request,"main/index.html")

def go_to_create_club_page(request):
    return redirect("create_club_page")

def go_to_create_account_page(request):
    return redirect("create_account_page")

def go_to_login_page(request):
    return redirect("login_page")

#after login display the user homepage
@login_required(login_url="login/")
def home(request,username):
    #check if the connected user is the same display in the URL
    if username != request.user.username:
        return redirect(reverse("home", kwargs={"username": request.user.username}))
    #else display his homepage
    return render(request, "main/home.html", {"username": request.user.username})



