from django.db import models
import json
class Room(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    playing = models.BooleanField(default=False)
    
    def __str__(self):
        return self.code
    
def get_default_room():
    return Room.objects.get_or_create(
        code = '0000',
    )
    
class Player(models.Model):
    sid = models.CharField(max_length=200, primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.SET(get_default_room))
    name = models.CharField(max_length=100)
    
    cards = models.TextField(default='')
    coins = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.name} ({self.room})'