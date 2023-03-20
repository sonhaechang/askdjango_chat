from django.conf import settings
from django.db import models


# Create your models here.
class Room(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_room_set'
    )

    name = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    @property
    def chat_group_name(self):
        return self.make_chat_gourp_name(room=self)
    
    @classmethod
    def make_chat_gourp_name(room=None, room_pk=None):
        return 'chat-%s' % (room_pk or room.pk)
    
    class Meta:
        ordering = ['-pk']