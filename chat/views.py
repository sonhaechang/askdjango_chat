from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from chat.forms import RoomForm
from chat.models import Room


# Create your views here.
def index(request):
    room_qs = Room.objects.all()

    return render(request, 'chat/container/index.html', {
        'room_list': room_qs,
    })


@login_required
def room_chat(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    return render(request, 'chat/container/room_chat.html', {
        'room': room,
    })


@login_required
def room_delete(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    if request.method == 'POST':
        if room.owner != request.user:
            messages.error(request, '채팅방 소유자가 아닙니다.')
        else:
            room.delete()
            messages.error(request, '채팅방을 삭제했습니다.')

        return redirect('chat:index')
    
    return render(request, 'chat/container/room_confirm_delete.html', {
        'room': room,
    })


@login_required
def room_new(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room = form.save(commit=False)
            created_room.owner = request.user
            created_room.save()
            return redirect('chat:room_chat', created_room.pk)
    else:
        form = RoomForm()

    return render(request, 'chat/container/room_new.html', {
        'form': form,
    })


@login_required
def room_users(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    # 현 채팅방에 새로운 접속 여부 체킹
    if not room.is_joined_user(request.user):
        return HttpResponse('Unauthorized user', status=401)
    
    username_list = room.get_online_usernames()

    return JsonResponse({'username_list': username_list})