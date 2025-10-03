from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Drill
from badges.models import Badge, UserBadge
from accounts.models import CustomUser
import copy

##############################
#
# ONLY IF A USER IS LOGGED IN
#
##############################

@login_required(login_url="login/")
def drills_log(request):
    """This view will redirect the user on his drills log and permit him to create/delete and read his drills"""

    #get the user drills and load them in a dict format {"key": value = all user drills} to render in the HTML 
    user_drills = Drill.objects.filter(user=request.user)
    all_user_drill = {"all_user_drill": user_drills}
    return render(request,"drills/drills_log.html",all_user_drill)


@login_required(login_url="login/")
def add_a_drill(request):
    """This view permit the user to create a drill"""
    
    if request.method == 'POST':
        name = request.POST.get("name")
        description = request.POST.get("description")
        #keyword is use for the badge acquisition (c.f: app drills view >> checkbox_drill)
        keyword = request.POST.get("keyword")
        if not name or not description:
            return HttpResponse("Paramètres manquants", status=400)
        #check if a drill with the same name exists (cannot have the same name for several drills)
        if Drill.objects.filter(name=name).exists():
            return HttpResponse("Un drill avec ce nom existe déjà", status=400)
        #create drill and save, reload the page to add more 
        drill = Drill(name=name,
                      description=description,
                      keyword=keyword,
                      user=request.user)
        drill.save()
    return render(request,"drills/add_drill.html")

@login_required(login_url="login/")
def checkbox_drill(request):
    """This view permit the user to delete drill or check if completed, using checkboxes"""

    if request.method == 'POST':
        #recieve all the id drills with checkboxes checked and the action use (delete/accomplish)
        drills_checked = request.POST.getlist("drill_check")
        action = request.POST.get("action")
        #delete the drills using ID
        if action == "delete":
            Drill.objects.filter(id__in=drills_checked,user=request.user).delete()
        #if the drill is done
        if action == "accomplish":
            #filter all the drills checked with checkboxes / all the badges unlocked by user / get all conditions from the badges locked (using filter > user badges unlocked)
            #condition format = dict >>> {"keyword"(e.g: 'SCISSOR SWEEP','CLOSED GUARD'...) : "count value" = an integer } >>> When all count values are 0 for a condition, 
            #condition is done
            drills = Drill.objects.filter(id__in=drills_checked,user=request.user)
            user_badges = UserBadge.objects.filter(user=request.user,is_completed=True).values_list("badge", flat=True)
            all_conditions = Badge.objects.exclude(id__in=user_badges).values_list("condition",flat=True)

            #iterate over each locked badge conditions and each drill checked to search if there are a match (using keyword)
            for condition in all_conditions:
                for drill in drills:
                    #if a match is find
                    if drill.keyword in condition:
                        #get the badge matching with conditions
                        badge = Badge.objects.get(condition=condition)
                        #if badge is already in progress for the user
                        try:
                            #get the badge and copy the actual progress to modify (count value - 1) using keyword
                            user_badge = UserBadge.objects.get(user=request.user, badge=badge,is_completed=False)
                            progress = copy.deepcopy(user_badge.progress)
                            progress[drill.keyword] -= 1
                            #check if all the count values in the progress dict are 0 >>> the badge is completed by user and add badge points at the user points
                            if all(progress.values()) == 0:
                                user = request.user
                                user.points += badge.point
                                user_badge.is_completed = True
                                user.save()
                            print(progress)
                            #after modification, update the badge progress and save him
                            user_badge.progress = progress
                            user_badge.save()

                        #if it's the first time, user in progress for this badge
                        except UserBadge.DoesNotExist:
                            #create and save new instance of the badge for this user 
                            new_badge = UserBadge.objects.create(user=request.user,badge=badge,is_completed=False)
                            new_badge.save()
                            #copy and update the badge condition (count value - 1) using keyword
                            badge_condition = copy.deepcopy(badge.condition)
                            badge_condition[drill.keyword] -= 1
                            #update the condition progress for this new badge
                            new_badge.progress = badge_condition
                            #check if all the count values in the progress dict are 0 >>> the badge is completed by user and add badge points at the user points
                            progress = copy.deepcopy(new_badge.progress)
                            if all(progress.values()) == 0:
                                user = request.user
                                user.points += badge.point
                                new_badge.is_completed = True
                                user.save()
                            new_badge.save()

            #whatever the results, delete all drills checked
            Drill.objects.filter(id__in=drills_checked,user=request.user).delete()
          
        return redirect("drills_log")

