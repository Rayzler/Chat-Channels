from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from .models import Room, Message


# Create your views here.
@login_required
def rooms(request):
    if request.method == "POST":
        room_name = request.POST.get("roomname")
        slug = f"{room_name}-{get_random_string(length=6)}"
        Room.objects.create(name=room_name, slug=slug)
        return redirect("rooms")

    _rooms = Room.objects.all()
    return render(request, "roomApp/rooms.html", {"rooms": _rooms})


@login_required
def room(request, slug):
    _room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=_room)
    return render(request, "roomApp/room.html", {"room": _room, "messages": messages})
