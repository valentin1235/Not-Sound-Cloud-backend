import jwt, bcrypt, json, uuid, requests

from django.db              import IntegrityError
from django.db.models       import Count, Q
from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.db              import IntegrityError
from django.core.exceptions import ValidationError
from django.db.utils        import DataError
from django.core.validators import validate_email
from django.core.validators import ValidationError

from .utils                    import login_required
from .models                   import User, Message, Follow, MessagePlaylist, MessageSong, GoogleAccount
from song.models               import Song, Playlist 
from notsoundcloud.my_settings import SECRET_KEY, ALGORITHM          

class WebSignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        if len(data['password']) < 8:
            return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
        
        if User.objects.filter(email=data['email']).exists():   
            return JsonResponse({'message' : 'USER_EXISTS'}, status = 400)

        try:
            validate_email(data['email'])
            User.objects.create(
                    email         = data['email'],
                    password      = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    age           = data['age'],
                    name          = data['name'],
                    gender        = data['gender'],
                    uuid          = str(uuid.uuid3(uuid.NAMESPACE_DNS, data['email']).hex)
            )
            token = jwt.encode({'user_id' : User.objects.get(email = data['email']).id}, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({'token' : token.decode()}, status = 200)

        except KeyError:            
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

        except IntegrityError:    
            return JsonResponse({'message' : 'USER_EXISTS'}, status = 400)

        except ValidationError:
            return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

class AppSignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        if len(data['password']) < 8:
            return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)

        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'message' : 'USER_EXISTS'}, status = 400)

        try:
            validate_email(data['email'])
            User.objects.create(
                    email    = data['email'],
                    password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    gender   = data['gender'],
                    age      = data['age'],
                    uuid     = str(uuid.uuid3(uuid.NAMESPACE_DNS, data['email']).hex)
            )
            token = jwt.encode({'user_id' : User.objects.get(email = data['email']).id}, SECRET_KEY, algorithm = ALGORITHM)
            return JsonResponse({'token' : token.decode()}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

        except IntegrityError:
            return JsonResponse({'message' : 'USER_EXISTS'}, status = 400)

        except ValidationError:
            return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
                
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode(
                        {'user_id' : User.objects.get(email = data['email']).id}, 
                        SECRET_KEY, 
                        algorithm = ALGORITHM
                    )
                    uuid = User.objects.get(email = data['email']).uuid
                    
                    return JsonResponse({'user' : {'token' : token.decode('utf-8'), 'uuid' : uuid}}, status = 200)

                return JsonResponse({'message' : 'CHECK_PASSWORD'}, status = 401)

            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

        except KeyError: 
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class MessageView(View):
    @login_required
    def post(self, request):
        data     = json.loads(request.body)
        playlist = data.get('playlist_id', None)
        song     = data.get('song_id', None)
        message  = Message.objects.create(
                content      = data['content'],
                from_user_id = request.user.id,
                to_user_id   = data['to_user_id'],
        )
    
        if playlist:
            MessagePlaylist.objects.create(
                message_id  = message.id,
                playlist_id = playlist,
            )

        if song:
            MessageSong.objects.create(
                message_id = message.id,
                song_id    = song,
            )

        return HttpResponse(status = 200)

    @login_required
    def get(self, request):
        try:
            filters = {'from_user_id' : request.user.id}
            to_user = request.GET.get('to_user', None)

            if to_user:
                filters['to_user_id'] = to_user
                messages = Message.objects.prefetch_related('playlist').filter(**filters)
                messages = [
                        {
                    'id'           : message.id, 
                    'content'      : message.content, 
                    'from_user_id' : message.from_user_id, 
                    'to_user_id'   : message.to_user.id, 
                    'created_at'   : message.created_at, 
                    'playlist'     : [{'playlist_id' : data.id, 'name' : data.name} for data in message.playlist.all()],
                    'song'         : [{'song_id' : data.id, 'name' : data.name} for data in message.song.all()],
                    }
                    for message in messages
                ]
            
                return JsonResponse({'data' : messages}, status = 200)
            
            messages = Message.objects.prefetch_related('playlist').filter(**filters)
            datas = [{
                    'from_user_id'      : message.from_user_id, 
                    'from_user_name'    : message.from_user.name, 
                    'to_user_id'        : message.to_user_id, 
                    'to_user_name'      : message.to_user.name,
                    'last_message'      : messages.last().content,
                    'last_message_time' : messages.last().created_at,} 
                    for message in messages]
            message_all = list({data['to_user_id'] : data for data in datas}.values())

            return JsonResponse({'data' : message_all}, status = 200)

        except ValueError:
            return JsonResponse({'message' : 'UNAUTHORIZED_USER'}, status = 403)

        except AttributeError:
            return JsonResponse({'message' : 'UNAUTHORIZED_USER'}, status = 403)

class FollowView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        user = request.user.id
        
        if user == data['to_follow_id']:
            return JsonResponse({'message' : 'SELF_FOLLOW'}, status = 400)
        
        if Follow.objects.filter(to_follow_id = data['to_follow_id']).exists():
            Follow.objects.filter(to_follow_id = data['to_follow_id']).delete()            
            return JsonResponse({'message' : 'UNFOLLOWED'}, status = 200)

        try:
            Follow.objects.create(
                from_follow_id = user,
                to_follow_id   = data['to_follow_id'],
            )
            
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

    @login_required
    def get(self, request):
        user           = request.user.id
        limit          = request.GET.get('limit', 3)
        user_following = Follow.objects.filter(from_follow_id=user)[:limit]
        to_follow = [{
            'id'             : data.to_follow.id, 
            'name'           : data.to_follow.name, 
            'song_count'     : data.to_follow.song_set.values().count(), 
            'follower_count' : data.to_follow.follow.values().count()} 
            for data in user_following]       

        return JsonResponse({'message' : to_follow})

class UserRecommendationView(View):
    @login_required
    def get(self, request):
        limit = request.GET.get('limit', 3)
        recommended_user = [
            {'name'           : user.name,
            'id'              : user.id, 
            'song_count'      : user.song_set.count(), 
            'to_follow_count' : user.follow.values().count()} 
            for user in User.objects.prefetch_related('follow').order_by('?')[:limit]
        ]

        return JsonResponse({'data' : recommended_user}, status = 200)


