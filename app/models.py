from django.db import models

from app.mixins import ChannelLayerGroupSendMixin

# Create your models here.
class Post(ChannelLayerGroupSendMixin, models.Model):
    CHANNEL_LAYER_GROUP_NAME = 'liveblog'

    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        ordering = ['-id']