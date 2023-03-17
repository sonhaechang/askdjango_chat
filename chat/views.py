from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'chat/container/index.html')


def room_chat(request, room_name):
    return render(request, 'chat/container/room_chat.html', {
        'room_name': room_name,
    })