import jwt, bcrypt, json, uuid

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
from .models                   import User, Message, Follow, MessagePlaylist, MessageSong
from music.models              import Song, Playlist 
from notsoundcloud.my_settings import SECRET_KEY, ALGORITHM          

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        if len(data['password']) < 8:
        
            return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)

        try:
            validate_email(data['email'])
            
            User.objects.create(
                    email         = data['email'],
                    password      = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    age           = data['age'],
                    name          = data['name'],
                    gender        = data['gender'],
                    profile_image = data['profile_image'],
                    uuid          = str(uuid.uuid3(uuid.NAMESPACE_DNS, data['email']).hex)
            )
            
            return HttpResponse(status = 200)

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
                    token = jwt.encode({'user_id' : User.objects.get(email = data['email']).id}, SECRET_KEY, algorithm = ALGORITHM)
                    uuid = User.objects.get(email = data['email']).uuid
                    
                    return JsonResponse({'user' : {'token' : token.decode('utf-8'), 'uuid' : uuid}}, status = 200)

                return JsonResponse({'message' : 'CHECK_PASSWORD'}, status = 401)

            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

        except KeyError:
        
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class MessageView(View):
    @login_required
    def post(self, request):
        data    = json.loads(request.body)
        message = Message.objects.create(
                content = data['content'],
                from_user_id = request.user.id,
                to_user_id   = data['to_user_id'],
        )

        try:
            MessagePlaylist.objects.create(
                    message_id  = message.id,
                    playlist_id = data['playlist_id'],
            )
        
        except :
            pass

        try:
            MessageSong.objects.create(
                    message_id = message.id,
                    song_id    = data['song_id'],
            )
        
        except :
            pass



        return HttpResponse(status = 200)

    @login_required
    def get(self, request):
        try:
            filters = {'from_user_id' : request.user.id}
            to_user = request.GET.get('to_user', None)

            if to_user is not None:
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
            
            if to_user is None:
                messages = Message.objects.prefetch_related('playlist').filter(**filters)
                datas = [{
                    'from_user_id' : message.from_user_id, 
                    'from_user_name' : message.from_user.name, 
                    'to_user_id' : message.to_user_id, 
                    'to_user_name' : message.to_user.name} 
                    for message in messages]
                message_all = list({data['to_user_id']: data for data in datas}.values())

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
        if user == data['followee_id']:
            return JsonResponse({'message' : 'SELF_FOLLOWING'}, status = 400)

        Follow.objects.create(
                follower_id = user,
                followee_id = data['followee_id'],
        )
        
        return HttpResponse(status = 200)















>>>>>>> 56d30bb... signup, signin unit test
