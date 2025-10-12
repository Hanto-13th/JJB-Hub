from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from accounts.models import Club


#the views to redirect to the page for login/create_club/create_user
def index(request):
    return render(request,"main/index.html")

def go_to_create_club_page(request):
    return redirect("create_club_page")

def go_to_create_account_page(request):
    return redirect("create_account_page")

def go_to_login_page(request):
    return redirect("login_page")

##############################
#
# ONLY IF A USER IS LOGGED IN
#
##############################

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

#render the user settings
@login_required(login_url="login/")
def user_settings(request):
    """This view will display the settings user can modify"""

    context = {"club": request.user.club.secret_key,
               "fav_submission": request.user.fav_submission,
               "fav_passage": request.user.fav_passage,
               "fav_guard": request.user.fav_guard}
    return render(request,"main/user_settings.html",context=context)

@login_required(login_url="login/")
def change_password(request):
    """This view will permit the user modify his password"""

    if request.method == 'POST':
        user = request.user
        new_password = request.POST.get("password")
        if not new_password:
            return HttpResponse("Mot de passe manquant", status=400)
        #using set password the new password is automatically encrypted
        user.set_password(new_password)
        user.save()
        #let the user session active after the password change
        update_session_auth_hash(request, user)
        return redirect("user_settings")
    return HttpResponse("Méthode non autorisée", status=405)

@login_required(login_url="login/")
def change_club(request):
    """This view will permit the user modify his club (remplacing the old secret_key by the new)"""

    if request.method == 'POST':
        user = request.user
        new_key = request.POST.get("secret_key")
        if not new_key:
            return HttpResponse("Clé secrète manquante", status=400)
        #check if the new club exists
        try:
            club = Club.objects.get(secret_key=new_key)
        except Club.DoesNotExist:
            return HttpResponse("Club introuvable", status=404)
        #if exists change for user and save
        user.club = club
        user.save()
        return redirect("user_settings")
    return HttpResponse("Méthode non autorisée", status=405)

@login_required(login_url="login/")
def change_favorite(request):
    """This view will permit the user modify his favorites"""

    if request.method == 'POST':
        user = request.user
        new_submission = request.POST.get("fav_submission")
        new_passage = request.POST.get("fav_passage")
        new_guard = request.POST.get("fav_guard")
        if not new_submission or not new_passage or not new_guard:
            return HttpResponse("Paramètres manquants", status=400)
        user.fav_submission = new_submission
        user.fav_passage = new_passage
        user.fav_guard = new_guard
        user.save()
        return redirect("user_settings")
    return HttpResponse("Méthode non autorisée", status=405)


@login_required(login_url="login/")
def new_belt(request):
    """This view will permit the user update his belt when promoted and give him the points"""

    POINTS = 100
    all_belts = ["White","Blue","Purple","Brown","Black"]
    user = request.user
    user_belt = user.belt
    #check if the user has the last belt
    if user_belt == all_belts[-1]:
        return HttpResponse("Aucune ceinture supérieure existante",status=404)
    #if not promote him
    index = all_belts.index(user_belt)
    new_grade = all_belts[index + 1]
    user.belt = new_grade
    user.points += POINTS
    user.save()
    return redirect("home")

@login_required(login_url="login/")
def new_victory(request):
    """This view will permit the user update his competition victory and give him the points"""

    POINTS = 4
    user = request.user
    user.victory += 1
    user.points += POINTS
    user.save()
    return redirect("home")

@login_required(login_url="login/")
def new_medal(request):
    """This view will permit the user update his competition medals and give him the points"""
    
    GOLD_POINTS = 30
    SILVER_POINTS = 20
    BRONZE_POINTS = 10
    user = request.user
    medal = request.POST.get("medal")
    if medal == "gold":
        user.gold_medal += 1
        user.points += GOLD_POINTS
        user.save()
    if medal == "silver":
        user.silver_medal += 1
        user.points += SILVER_POINTS
        user.save()
    if medal == "bronze":
        user.bronze_medal += 1
        user.points += BRONZE_POINTS
        user.save()
    return redirect("home")
