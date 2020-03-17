from django.db import models

from song.models import Song
from user.models import User

class Comment(models.Model):
    content    = models.TextField()
    user       = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comment_user')
    song       = models.ForeignKey(Song, on_delete = models.CASCADE, related_name = 'song_user')
    position   = models.IntegerField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'comments'
