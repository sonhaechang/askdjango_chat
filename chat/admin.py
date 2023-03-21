from django.contrib import admin

from chat.models import Room, RoomMember


# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'owner', 'created_at', 'updated_at']
    list_display_links = ['pk', 'name']


@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'room']
    list_display_links = ['pk', 'user', 'room']
