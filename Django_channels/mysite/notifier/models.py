from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save  
from django.dispatch import receiver
# Create your models here.

class Camera(models.Model):
	cam_id = models.IntegerField(default=0)
	cam_status = models.CharField(max_length=20)
	trash = models.BooleanField(default=False)
	instrusion = models.BooleanField(default=False)
	fallen = models.BooleanField(default=False)
	cam_location = models.CharField(max_length=50)
	fence = models.BooleanField(default=False)
	weight = models.IntegerField(default=1)

# class Trash(models.Model):
# 	trash = models.BooleanField(default=False)

#class Detections(models.Model):
#	trashes = models.BooleanField(default=False)
#	instrusions = models.BooleanField(default=False)
#	fallen = models.BooleanField(default=False)
class Profile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    loginchk = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()
