async_mode = None

# django
import os
from django.http import HttpResponse
from django.shortcuts import render
import socketio

# coup
import random
import string

# models
from .models import Room, Player

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(
    async_mode=async_mode
)
thread = None

def index(request):
    return render(request, "coup/play.html")

def generate_code():
    a = [str(i) for i in list(Room.objects.all())]
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    if code in a or code == '0000':
        return generate_code()
    return code

@sio.event
def create_room(sid, message):
    code = generate_code()
    playing = False
    
    r = Room(
        code=code,
        playing=playing
    )
    r.save()
    
    p = Player(
        sid=sid,
        room=r,
        name=message['name'],
    )
    p.save()
    
    sio.enter_room(sid, code)
    sio.emit('my_response', {'data':f'Joined ROOM: {code}'}, room=sid)
    
@sio.event
def join_room(sid, message):
    code = message['code']
    r = Room.objects.get(pk=code)
    
    p = Player(
        sid=sid,
        room=r,
        name=message['name'],
    )
    p.save()
    
    sio.enter_room(sid, code)
    sio.emit('my_response', {'data':f'Joined ROOM: {code}'}, room=sid)
    
# connect / disconnect    
@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)

@sio.event
def connect(sid, environ):
    print(f'\033[1;34m{sid} CONNECTED', end='\n\033[0m')
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

@sio.event
def disconnect(sid):
    print('Client disconnected')