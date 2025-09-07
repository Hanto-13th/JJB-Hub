from django.db import models
from accounts.models import Users

#the class for each drill the users can create
class Drills(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    accomplish = models.BooleanField()
    creation_date = models.DateField()


