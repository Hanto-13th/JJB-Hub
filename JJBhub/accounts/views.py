from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import secrets
from .models import Club,CustomUser

#the views to display the page for login/create_club/create_user
def create_account_page(request):
    return render(request,"accounts/create_account.html")

def create_club_page(request):
    secret_key = {"secret_key":secrets.token_urlsafe(6)[:6]}
    return render(request,"accounts/create_club.html",secret_key)

def login_page(request):
    return render(request,"accounts/login.html")

#get alls infos from the label to create the club (only the club name, the key is automatically generated)
def create_a_club(request):
    if request.method == 'POST':
        name = request.POST.get("club_name")
        key = request.POST.get("secret_key")
        #check the infos required
        if not name or not key:
            return HttpResponse("Paramètres manquants", status=400)
        #create the club object and save him
        club = Club(club_name=name,secret_key=key)
        club.save()
        messages.success(request, f"Le club {name} a bien été créé !")
        return redirect("index")
    return HttpResponse("Méthode non autorisée", status=405)

#get alls infos from the label to create an user, hash the password to allows the creation
def create_an_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        club_key = request.POST.get("club_secret_key")
        belt = request.POST.get("belt")
        fav_submission = request.POST.get("fav_submission")
        fav_passage = request.POST.get("fav_passage")
        fav_guard = request.POST.get("fav_guard")

        if not username or not password or not club_key:
            return HttpResponse("Paramètres manquants", status=400)
        #check if they are a club matching with the secret key to allow the user connect with this club
        try:
            club = Club.objects.get(secret_key=club_key)
        except Club.DoesNotExist:
            return HttpResponse("Club introuvable", status=404)
        #if all good, create user and save him
        user = CustomUser(username=username,
                        password=make_password(password),
                        first_name=firstname,
                        last_name=lastname,
                        club=club,
                        belt=belt,
                        points=0,
                        fav_submission=fav_submission,
                        fav_passage=fav_passage,
                        fav_guard=fav_guard)
        user.save()

        messages.success(request, f"L'utilisateur {firstname+" "+lastname} a bien été créé !")
        return redirect("index")
    return HttpResponse("Méthode non autorisée", status=405)

#get the username and the password to connect into user session
def account_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            return HttpResponse("Paramètres manquants", status=400)
        user = authenticate(username=username, password=password)
        #if not user with this ID redirect to the login
        if user is None:
            messages.success(request,"Utilisateur Introuvable")
            return redirect("login_page")
        #else login him and redirect to his homepage
        login(request,user)
        messages.success(request,"Vous vous êtes connecté avec succès !")
        return redirect("home")

    return HttpResponse("Méthode non autorisée", status=405)

@login_required(login_url="login/")
def account_logout(request):
    logout(request)
    return redirect("login_page")







        




