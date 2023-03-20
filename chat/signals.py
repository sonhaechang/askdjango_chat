from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.db.models.signals import post_delete
from django.dispatch import receiver

from chat.models import Room


@receiver(post_delete, sender=Room)
def on_post_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        instance.chat_group_name,
        {
            "type": "chat.room.deleted",
        }
    )