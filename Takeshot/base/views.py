from django import forms
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#    {'id':1,'name':'Lets learn python!'},
#    {'id':2,'name':'Design with me'},
#    {'id':3,'name':'Frondend developer'},
# ]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # used for search rooms
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))

    topics = Topic.objects.all() # to take all the topic
    room_count = rooms.count() # for counting rooms

    context = {'rooms': rooms,'topics':topics,'room_count':room_count} #sending data to website
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)  # pk is the number in url in the path
    context = {'room': room}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)  # pk is the number in url in the path
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})
