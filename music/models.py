
from django.db import models

class Song(models.Model):
    name = models.CharField(max_length = 45, null = True)
    
    class Meta:
        db_table = 'songs'

class Playlist(models.Model):
    name = models.CharField(max_length = 45, null = True)
        
    class Meta:
        db_table = 'playlists'
