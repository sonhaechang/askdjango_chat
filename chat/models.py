from django.conf import settings
from django.db import models

from config.json_extended import ExtendedJSONDecoder, ExtendedJSONEncoder


# Create your models here.
class OnlineUserMixin(models.Model):
    online_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='chat.RoomMember',
        related_name='joined_room_set',
        blank=True
    )

    def get_online_users(self):
        ''' 현 Room에 접속중인 User 쿼리셋을 반환 '''

        return self.online_user_set.all()
    
    def get_online_usernames(self):
        qs = self.get_online_users().values_list('username', flat=True)
        return list(qs)
    
    def is_joined_user(self, user):
        ''' 지정 User가 현 Room의 접속 여부를 반영 '''

        return self.get_online_users().filter(pk=user.pk).exists()
    
    def user_join(self, channel_name, user):
        ''' 현 Room에 최초 접속 여부를 반환 '''

        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            room_member = RoomMember(room=self, user=user)

        is_new_join = len(room_member.channel_names) == 0
        room_member.channel_names.add(channel_name)

        if room_member.pk is None:
            room_member.save()
        else:
            room_member.save(update_fields=['channel_names'])

        return is_new_join
    
    def user_leave(self, channel_name, user):
        ''' 현 Room으로부터 최종 접속종료 여부를 반환 '''

        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            return True
        
        room_member.channel_names.remove(channel_name)

        if not room_member.channel_names:
            room_member.delete()
            return True
        else:
            room_member(update_fields=['channel_names'])
            return False

    class Meta:
        abstract = True


class Room(OnlineUserMixin, models.Model):
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
        return self.make_chat_group_name(room=self)

    @staticmethod
    def make_chat_group_name(room=None, room_pk=None):
        return "chat-%s" % (room_pk or room.pk)
    
    class Meta:
        ordering = ['-pk']


class RoomMember(models.Model):
    # 하나의 User가 하나의 Room 간의 관계를 1회 저장한다.
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    room = models.ForeignKey(
        to='chat.Room',
        on_delete=models.CASCADE
    )

    '''
    하나의 User가 하나의 Room에 대해, 다수의 접속이 있을 수 있다.
    각 접속에서의 채널명 목록을 집합으로 저장하여, 최초접속 및 최종 접속종료를 인지토록 한다.
    디폴트로 빈 집합이 생성되도록 한다. 
    '''

    channel_names = models.JSONField(
        default=set,
        encoder=ExtendedJSONEncoder,
        decoder=ExtendedJSONDecoder 
    )

