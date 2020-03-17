import jwt, bcrypt, json, uuid, pytest

from user.utils                import login_required
from .models                   import Comment
from user.models               import User
from comment.views             import CommentView
from song.models               import Song, Playlist
from notsoundcloud.my_settings import SECRET_KEY, ALGORITHM

from django.test import TestCase, Client

class SignUpTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email         = 'aaa@aaa.com',
            password      = 'aaaaaaaa',
            age           = '28',
            name          = 'heechul',
            gender        = 'Male',
            profile_image = 'aaaaaaaa',
        )

        self.token = jwt.encode({'user_id' : self.user.id}, SECRET_KEY, algorithm = ALGORITHM)

        self.song = Song.objects.create(
            name        = 'lalala',
            description = 'lalala',
            song_url    = 'http://lalala',
        )

        self.comment = Comment.objects.create(
            user_id  = self.user.id,
            song_id  = 1,
            content  = 'not bad',
            position = 32
        )    
        
    def tearDown(self):
        User.objects.all().delete()
        Song.objects.all().delete()
        Comment.objects.all().delete()

    def test_comment_get_comment_success(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}
        response = client.get(f'/comment/{self.song.id}', **header)
        self.assertEqual(response.status_code, 200)

    def test_comment_post_success(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token}
        comment = {
                'song_id'  : 1,
                'content'  : 'not bad',
                'position' : 32,
        }
        response = client.post(f'/comment/{self.song.id}', json.dumps(comment), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

