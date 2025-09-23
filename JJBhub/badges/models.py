from django.db import models

#the class for each badges the users can receive with relation Many to Many for users
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    condition = models.CharField(max_length=200)
    point = models.IntegerField()
    obtention_date = models.DateField()

    def __str__(self):
        return self.name



