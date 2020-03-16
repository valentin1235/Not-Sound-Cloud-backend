import jwt, bcrypt, json, uuid, pytest

from .utils                    import login_required
from .models                   import User, Message, Follow, MessagePlaylist, MessageSong
from .views                    import SignInView, WebSignUpView, MessageView, FollowView 
from song.models               import Song, Playlist
from notsoundcloud.my_settings import SECRET_KEY, ALGORITHM

from django.test import TestCase, Client

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            email         = 'aaa@aaa.com',
            password      = 'aaaaaaaa',
            age           = '28',
            name          = 'heechul',
            gender        = 'Male',
            profile_image = 'aaaaaaaa',
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_sign_up_success(self):
        user = {
            'email'         : 'heechul@heechul.com',
            'password'      : 'heechulheechul',
            'age'           : '28',
            'name'          : 'heechul',
            'gender'        : 'male',
            'profile_image' : 'heechul'
        }

        client   = Client()
        response = client.post('/user/sign-up', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_sign_up_key_error(self):
        user = {
            'email'         : 'heechul@heechul.com',
            'password'      : 'heechulheechul',
            'name'          : 'heechul',
            'gender'        : 'male',
            'profile_image' : 'heechul'
        }

        client   = Client()
        response = client.post('/user/sign-up', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_KEY'})

    def test_sign_up_user_exists(self):
        user = {
            'email'         : 'aaa@aaa.com',
            'password'      : 'aaaaaaaa',
            'name'          : 'heechul',
            'age'           : '28',
            'gender'        : 'male',
            'profile_image' : 'heechul'
        }

        client   = Client()
        response = client.post('/user/sign-up', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'USER_EXISTS'})

    def test_sign_up_invalid_password_case(self):
        user = {
            'email'         : 'heechul@heechul.com',
            'password'      : 'heechul',
            'name'          : 'heechul',
            'gender'        : 'male',
            'profile_image' : 'heechul'
        }

        client   = Client()
        response = client.post('/user/sign-up', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_PASSWORD'})

    def test_sign_up_validation_error(self):
        user = {
            'email'         : 'heechulheechulcom',
            'password'      : 'heechulheechul',
            'name'          : 'heechul',
            'gender'        : 'male',
            'profile_image' : 'heechul'
        }

        client   = Client()
        response = client.post('/user/sign-up', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_EMAIL'})

class SignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            email         = 'heechuls@heechuls.com',
            password      = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            age           = 28,
            name          = 'heechul',
            gender        = 'Male',
            profile_image = 'aaaaaaaa',
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_sign_in_success(self):
        client = Client()
        user   = {
            'email'    : 'heechuls@heechuls.com',
            'password' : '12345678',
        }
        response = client.post('/user/sign-in', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        
    def test_sign_in_check_password_case(self):
        client = Client()
        user   = {
            'email'    : 'heechuls@heechuls.com',
            'password' : '1234567',
        }
        response = client.post('/user/sign-in', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'CHECK_PASSWORD'})
        
    def test_sign_in_invalid_user_case(self):
        client = Client()
        user   = {
            'email'    : 'heechuls@heechul.com',
            'password' : '12345678',
        }
        response = client.post('/user/sign-in', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'INVALID_USER'})

    def test_sign_in_Key_error(self):
        client = Client()
        user   = {
            'email'    : 'heechuls@heechuls.com',
        }
        response = client.post('/user/sign-in', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_KEY'})

class MessageTest(TestCase):
    def setUp(self):
        User.objects.create(email='aaa@aaa.com', password='aaaaaaaa', name='aaa', gender='male', profile_image='aaa')
        User.objects.create(email='bbb@bbb.com', password='bbbbbbbb', name='bbb', gender='male', profile_image='bbb')
        Playlist.objects.create(name='good')
        Song.objects.create(name='hi', user_id=1)
        self.token = jwt.encode({'user_id' : User.objects.get(email = 'aaa@aaa.com').id}, SECRET_KEY, algorithm = ALGORITHM)
        self.message = Message.objects.create(
                content = 'hi',
                from_user_id = 1,
                to_user_id = 2,
        )

    def tearDown(self):
        User.objects.all().delete()
        Message.objects.all().delete()
        Playlist.objects.all().delete()
        Song.objects.all().delete()

    def test_message_get_all_message_success(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}
        response = client.get('/user/message', **header)
        self.assertEqual(response.status_code, 200)

    def test_message_get_to_user_message_success(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}
        response = client.get('/user/message?to_user=2', **header)
        self.assertEqual(response.status_code, 200)

    def test_message_post_success(self):
        client  = Client()
        header  = {"HTTP_Authorization" : self.token}
        message = {
                'from_user_id' : 1,
                'to_user_id'   : 2,
                'content'      : 'how are you',
                'playlist_id'  : 1,
                'song_id'      : 2,
        }
        response = client.post('/user/message', json.dumps(message), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

class FollowTest(TestCase):
    def setUp(self):
        User.objects.create(email='aaa@aaa.com', password='aaaaaaaa', name='aaa', gender='male', profile_image='aaa')
        User.objects.create(email='bbb@bbb.com', password='bbbbbbbb', name='bbb', gender='male', profile_image='bbb')        
        User.objects.create(email='ccc@ccc.com', password='cccccccc', name='ccc', gender='male', profile_image='ccc')
        Follow.objects.create(from_follow_id = 1, to_follow_id=2)
        self.token = jwt.encode({'user_id' : User.objects.get(email = 'aaa@aaa.com').id}, SECRET_KEY, algorithm = ALGORITHM)
        
    def tearDown(self):
        User.objects.all().delete()
        Follow.objects.all().delete()

    def test_follow_post_follow_success(self):
        client = Client()
        header = {"HTTP_Authorization" : self.token}
        follow = {
                'to_follow_id' : 3,
        }
        response = client.post('/user/follow', json.dumps(follow), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_follow_post_unfollow_success(self):
        client = Client()
        header = {"HTTP_Authorization" : self.token}
        follow = {
                'to_follow_id' : 2,
        }
        response = client.post('/user/follow', json.dumps(follow), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'UNFOLLOWED'})

    def test_follow_get_success(self):
        client = Client()
        header = {"HTTP_Authorization" : self.token}
        response = client.get('/user/follow', **header)
        self.assertEqual(response.status_code, 200)

class UserRecommendationTest(TestCase):
    def setUp(self):
        User.objects.create(email='aaa@aaa.com', password='aaaaaaaa', name='aaa', age='24', gender='male')
        User.objects.create(email='bbb@bbb.com', password='bbbbbbbb', name='bbb', age='24', gender='male')
        self.token = jwt.encode({'user_id' : User.objects.get(email = 'aaa@aaa.com').id}, SECRET_KEY, algorithm = ALGORITHM)

    def test_get_success(self):
        client = Client()
        header = {"HTTP_Authorization" : self.token}
        response = client.get('/user/recommendation', **header)
        self.assertEqual(response.status_code, 200)






