from django.db import models
from django.conf import settings

#the class for each badges the users can receive with relation Many to Many for users
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    condition = models.JSONField(default=dict, blank=True)
    point = models.IntegerField()
    image_path = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
    
class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    obtention_date = models.DateField(auto_now_add=True)
    progress = models.JSONField(default=dict)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.badge.name +" - "+ self.user.first_name +" "+ self.user.last_name



