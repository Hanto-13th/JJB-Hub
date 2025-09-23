from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


#the views to redirect to the page for login/create_club/create_user
def index(request):
    return render(request,"main/index.html")

def go_to_create_club_page(request):
    return redirect("create_club_page")

def go_to_create_account_page(request):
    return redirect("create_account_page")

def go_to_login_page(request):
    return redirect("login_page")

########################
#
# ONLY IF A USER IS LOG
#
########################

#after login display the user homepage
@login_required(login_url="login/")
def home(request):
    """This view will display the homepage of each user with all their informations"""
    
    context = {"username": request.user.username,
                "firstname": request.user.first_name,
               "belt": request.user.belt,
               "club": request.user.club.club_name,
               "points": request.user.points,
               "victory": request.user.victory,
               "gold_medal": request.user.gold_medal,
               "silver_medal": request.user.silver_medal,
               "bronze_medal": request.user.bronze_medal,
               "fav_submission": request.user.fav_submission,
               "fav_passage": request.user.fav_passage,
               "fav_guard": request.user.fav_guard}
    return render(request, "main/home.html", context=context)





