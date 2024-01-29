from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.
@login_required
def chatroom(request):
    rooms = Room.objects.all()
    return render(request, 'base.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Massage.objects.filter(room=room)[0:25]
    return render(request, 'room.html', {"room": room, "messages":messages})

@login_required
def roomboard(request):
    rooms = Room.objects.all()
    return render(request, 'chatroom.html', {'rooms': rooms})

@login_required
def base(request):
    rooms = Room.objects.all()
    return render(request, 'base.html', {'rooms': rooms})

