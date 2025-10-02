from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserBadge, Badge

##############################
#
# ONLY IF A USER IS LOGGED IN
#
##############################

@login_required(login_url="login/")
def badges_page(request):
    #get all the badges unlocked by user and all badges existing to render in HTML template
    badge_names = list(UserBadge.objects.filter(user=request.user,is_completed=True).values_list("badge__name", flat=True))
    all_badges_existing = Badge.objects.all()
    context = {"user_badge_names": badge_names, "all_badges": all_badges_existing}
    return render(request,"badges/badges_page.html",context)

