from django.db import models
from badges.models import Badges


class Clubs(models.Model):
    club_name = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=6)
    creation_date = models.DateField()

class Users(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    belt = models.IntegerField()
    badges = models.ManyToManyField(Badges)
    points = models.IntegerField()
    stats = models.CharField(max_length=500)
    creation_date = models.DateField()

class Login(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=20)
    user = models.OneToOneField(Users)





