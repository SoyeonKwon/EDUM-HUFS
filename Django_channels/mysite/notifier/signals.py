from . import threading
import time
from .models import Camera
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from. import send

@receiver(post_save, sender=Camera)
def popup_handler(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "cameras", {"type": "cam_message",
                       "event": "created",
                       "cam_id": instance.cam_id,
			"cam_location": instance.cam_location,
                        "trash": instance.trash,
                        "instrusion": instance.instrusion,
                        "fence" : instance.fence,
                        "fallen": instance.fallen
                        })
    elif instance.cam_status == 'warning':
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "cameras", {"type": "cam_message",
                        "event": "warning",
                        "cam_id": instance.cam_id,
                        "cam_location": instance.cam_location,
                        "trash": instance.trash,
                        "instrusion": instance.instrusion,
                        "fence" : instance.fence,
                        "fallen": instance.fallen})
#     event_handler(sender, instance)
#
# def event_handler(sender, instance,**kwargs):
#     if instance.fallen == True:
#         print("Fallen_detect")
#         instance.cam_status = 'warning'
#         instance.weight += 2
#
#     if instance.trash == True:
#         print("trash_detect")
#         instance.cam_status = 'warning'
#         instance.weight += 1
#
#     if instance.fence == True:
#         print("fence_pass")
#         instance.cam_status = 'warning'
#         instance.weight += 3
#
#     if instance.instrusion == True:
#         print("intrusion_pass")
#         instance.cam_status = 'warning'
#         instance.weight += 3