import jwt, bcrypt, json, uuid

from django.db.models       import Count, Q

from .utils                    import login_required
from .models                   import User, Message, Follow, MessagePlaylist, MessageSong
from music.models              import Song, Playlist
from notsoundcloud.my_settings import SECRET_KEY, ALGORITHM

from django.test import TestCase, Client

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
                    email         = 'aaa@aaa.com',
                    password      = 'aaaaaaaa',
                    age           = 28,
                    name          = 'heechul',
                    gender        = 'Male',
                    profile_image = 'aaaaaaaa',
        )

    def test_sign_up_success(self):
        user = {
            'email'         : 'heechul@heechul.com',
            'password'      : 'heechulheechul',
            'age'           : '28',
            'name'          : 'heechul',
            'gender'        : 'male',
            'profile_image' : 'heechul'
        }

        client = Client()
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

        client = Client()
        response = client.post('/user/sign-up', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_KEY'})

    def test_sign_up_integrity_error(self):
        user = {
            'email'         : 'heechul@heechul.com',
            'password'      : 'heechulheechul',
            'name'          : 'heechul',
            'gender'        : 'male',
            'profile_image' : 'heechul'
        }

        client = Client()
        response = client.post('/user/sign-up', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_KEY'})

    def test_sign_up_invalid_password_case(self):
        user = {
            'email'         : 'heechul@heechul.com',
            'password'      : 'heechul',
            'name'          : 'heechul',
            'gender'        : 'male',
            'profile_image' : 'heechul'
        }

        client = Client()
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

        client = Client()
        response = client.post('/user/sign-up', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_EMAIL'})

    def tearDown(self):
        User.objects.all().delete()


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
        





>>>>>>> 56d30bb... signup, signin unit test
