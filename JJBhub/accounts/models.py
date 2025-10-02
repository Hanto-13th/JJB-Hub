from django.db import models
from django.contrib.auth.models import AbstractUser
    
#the Clubs has a access by secret key (Generated 6 random character)
class Club(models.Model):
    club_name = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=6)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.club_name 

#all the Users settings and relation between the club, the drills and the badges
class CustomUser(AbstractUser):
    BELT_CHOICES = [
    ("White", "White"),
    ("Blue", "Blue"),
    ("Purple", "Purple"),
    ("Brown", "Brown"),
    ("Black", "Black")]
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    belt = models.CharField(max_length=10,choices=BELT_CHOICES,default="White")
    badges = models.ManyToManyField("badges.Badge",through="badges.UserBadge",blank=True)
    points = models.IntegerField(default=0)
    victory = models.IntegerField(default=0)
    gold_medal = models.IntegerField(default=0)
    silver_medal = models.IntegerField(default=0)
    bronze_medal = models.IntegerField(default=0)
    fav_submission = models.CharField(max_length=250,default="")
    fav_passage = models.CharField(max_length=250,default="")
    fav_guard = models.CharField(max_length=250,default="")
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        complete_name = self.first_name +" "+ self.last_name
        return complete_name







