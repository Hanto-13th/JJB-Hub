from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Drill

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
        if not name or not description:
            return HttpResponse("Paramètres manquants", status=400)
        #check if a drill with the same name exists (cannot have the same name for several drills)
        if Drill.objects.filter(name=name).exists():
            return HttpResponse("Un drill avec ce nom existe déjà", status=400)
        drill = Drill(name=name,
                      description=description,
                      accomplish = False,
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
        #Work in progress
        if action == "accomplish":
            Drill.objects.filter(id__in=drills_checked,user=request.user).delete()
        return redirect("drills_log")

