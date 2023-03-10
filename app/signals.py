from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse

from app.models import Post


@receiver(post_save, sender=Post)
def on_post_save(sender, instance, created, **kwargs):
    if created:
        message_type = 'liveblog.post.created'
    else:
        message_type = 'liveblog.post.updated'

    post_id = instance.pk
    post_partial_url = reverse('post_partial', args=[post_id])

    instance.channel_layer_group_send({
        'type': message_type,
        'post_id': post_id,
        'post_partial_url': post_partial_url,
    })


@receiver(post_delete, sender=Post)
def on_post_delete(sender, instance, **kwargs):
    post_id = instance.pk

    instance.channel_layer_group_send({
        'type': 'liveblog.post.deleted',
        'post_id': post_id,
    })