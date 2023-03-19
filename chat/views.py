from django.shortcuts import render, redirect, get_object_or_404

from chat.forms import RoomForm
from chat.models import Room


# Create your views here.
def index(request):
    return render(request, 'chat/container/index.html')


def room_new(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            new_room = form.save()
            return redirect('chat:room_chat', new_room.pk)
    else:
        form = RoomForm()

    return render(request, 'chat/container/room_new.html', {
        'form': form,
    })


def room_chat(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    
    return render(request, 'chat/container/room_chat.html', {
        'room': room,
    })