from django.db import models
from accounts.models import CustomUser

#the class for each drill the users can create with relation Many to One for users
class Drill(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accomplish = models.BooleanField()
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


