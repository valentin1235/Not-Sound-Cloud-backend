from django.db import models

class Song(models.Model):
    name        = models.CharField(max_length = 45)
    description = models.TextField()
    small_image = models.URLField(null = True)
    big_image   = models.URLField(null = True)
    song_url    = models.URLField(null = True)
    album       = models.ForeignKey('Album', on_delete = models.SET_NULL, null = True)
    option      = models.ForeignKey('Option', on_delete = models.SET_NULL, null = True)
    user        = models.ForeignKey('user.User', on_delete = models.SET_NULL, null = True)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'songs'

class Album(models.Model):
    name        = models.CharField(max_length = 45)
    description = models.TextField(null=True)
    option      = models.ForeignKey('Option', on_delete = models.SET_NULL, null = True)
    user        = models.ForeignKey('user.User', on_delete = models.SET_NULL, null = True)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'albums'

class Playlist(models.Model):
    name        = models.CharField(max_length=45)
    user        = models.ForeignKey('user.User', on_delete = models.SET_NULL, null = True)
    option      = models.ForeignKey('Option', on_delete = models.SET_NULL, null = True)
    is_popular  = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    song        = models.ManyToManyField('Song',through='PlaylistSong')
    class Meta:
        db_table = 'playlists'


class Option(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'options'

class PlaylistSong(models.Model):
    song     = models.ForeignKey('Song',on_delete=models.SET_NULL,null=True)
    playlist = models.ForeignKey('Playlist',on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table = 'playlist_songs'

class Tag(models.Model):
    name     = models.CharField(max_length=45)
    album    = models.ManyToManyField('Album',through='TagAlbum')
    playlist = models.ManyToManyField(Playlist,through='TagPlaylist')
    song     = models.ManyToManyField(Song,through='TagSong')
    class Meta:
        db_table='tags'

class TagAlbum(models.Model):
    album = models.ForeignKey('Album', on_delete = models.SET_NULL, null = True)
    tag   = models.ForeignKey('Tag', on_delete = models.SET_NULL,null = True)
    class Meta:
        db_table='tag_albums'

class TagPlaylist(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete = models.SET_NULL, null = True)
    tag      = models.ForeignKey('Tag', on_delete = models.SET_NULL,null = True)
    class Meta:
        db_table='tag_playlists'

class TagSong(models.Model):
    song  = models.ForeignKey('Song', on_delete = models.SET_NULL, null = True)
    tag   = models.ForeignKey('Tag', on_delete = models.SET_NULL,null = True)                  
    class Meta:
        db_table='tag_songs'
