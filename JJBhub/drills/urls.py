from django.urls import path
from . import views

urlpatterns = [
    path("home/drills_log/", views.drills_log, name="drills_log"),
    path("home/drills_log/add", views.add_a_drill, name="add_drill"),
]