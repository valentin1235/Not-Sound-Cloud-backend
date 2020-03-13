import uuid
import datetime

from django.utils import timezone
from django.db import models
from django.core.validators import MinLengthValidator

from music.models import Song, Playlist

class User(models.Model):
    email         = models.EmailField(max_length = 250, null = True, unique = True)
    password      = models.CharField(validators = [MinLengthValidator(8)], max_length = 100, unique = True)
    age           = models.CharField(max_length = 100, null = True)
    name          = models.CharField(max_length = 50, null = True)
    gender        = models.CharField(max_length = 5, null = True)
    profile_image = models.CharField(max_length = 100, null = True)
    grade         = models.ForeignKey('Grade', on_delete = models.CASCADE, null = True, default = 1)
    uuid          = models.CharField(max_length = 200, null = True, unique = True)
    message       = models.ManyToManyField('self', through = 'Message', symmetrical = False, related_name = 'message_reverse')
    follow        = models.ManyToManyField('self', through = 'Follow', symmetrical = False, related_name = 'follow_reverse')
    created_at    = models.DateTimeField(auto_now_add=True, null=True)
    updated_at    = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'users'

class Grade(models.Model):
    grade_name = models.CharField(max_length = 45, unique = True)

    class Meta:
        db_table = 'grades'

class Message(models.Model):
    content    = models.TextField(null = True)
    from_user  = models.ForeignKey('User', on_delete = models.SET_NULL, null = True, related_name = 'from_user')
    to_user    = models.ForeignKey('User', on_delete = models.SET_NULL, null = True, related_name = 'to_user')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    playlist   = models.ManyToManyField(Playlist, through = 'MessagePlaylist')
    song       = models.ManyToManyField(Song, through = 'MessageSong')

    class Meta:
        db_table        = 'messages'

class MessagePlaylist(models.Model):
    message  = models.ForeignKey('Message', on_delete = models.CASCADE, null = True)
    playlist = models.ForeignKey(Playlist, on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'message_playlists'

class MessageSong(models.Model):
    message = models.ForeignKey('Message', on_delete = models.CASCADE, null = True)
    song    = models.ForeignKey(Song, on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'message_songs'

class Follow(models.Model):
    follower = models.ForeignKey('User', on_delete = models.CASCADE, null = True, related_name = 'follower')
    followee = models.ForeignKey('User', on_delete = models.CASCADE, null = True, related_name = 'followee')
    
    class Meta:
        unique_together = ('follower', 'followee')
        db_table = 'follows'


>>>>>>> 56d30bb... signup, signin unit test
