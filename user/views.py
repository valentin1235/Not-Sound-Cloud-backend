import jwt, bcrypt, json, uuid, requests

from django.db              import IntegrityError, transaction, connection
from django.db.models       import Count, Q
from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.db              import IntegrityError
from django.core.exceptions import ValidationError
from django.db.utils        import DataError
from django.core.validators import validate_email
from django.core.validators import ValidationError

from .utils                    import login_required
from .models                   import User, Message, MessageNumber, Follow, MessagePlaylist, MessageSong
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
            user = User.objects.create(
                    email         = data['email'],
                    password      = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    age           = data['age'],
                    name          = data['name'],
                    gender        = data['gender'],
                    uuid          = str(uuid.uuid3(uuid.NAMESPACE_DNS, data['email']).hex)
            )
            token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm = ALGORITHM).decode()

            return JsonResponse({'token' : token}, status = 200)

        except KeyError:            
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

        except IntegrityError as e:    
            return JsonResponse({'message' : f'{e}'}, status = 400)

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
                    uuid = user.uuid
                    return_key = {'user' : {'token' : token.decode('utf-8'), 'uuid' : uuid}}

                    return JsonResponse(return_key, status = 200)

                return JsonResponse({'message' : 'CHECK_PASSWORD'}, status = 401)

            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

        except KeyError: 
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class UserSearchView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        users = User.objects.filter(name = data['name'])
        user_info = [{'user_id' : user.id, 'user_name' : user.name} for user in users]
        
        return JsonResponse({'user_info' : user_info}, status = 200)

class MessageView(View):
    @login_required
    def post(self, request):
        data         = json.loads(request.body)
        content      = data.get('content', None)
        user = request.user
        if not content:
            return JsonResponse({'message' : 'CONTENT_MISSING'}, status = 400)

        to_user_id = data.get('to_user_id', None)
        if not to_user_id:
            return JsonResponse({'message' : 'TO_USER_ID_MISSING'}, status = 400)
              
        message_number_id = data.get('message_number_id', None) 
        if Message.objects.filter((Q(to_user_id = to_user_id)&Q(from_user_id = user.id)&Q(message_number_id = message_number_id))|(Q(to_user_id = user.id)&Q(from_user_id = to_user_id)&Q(message_number_id = message_number_id))).exists():

            if not message_number_id:
                return JsonResponse({'message' : 'MESSAGE_NUMBER_ID_NEEDED'}, status = 400)
            
            message = Message.objects.create(
                message_number_id = message_number_id,
                content        = content,
                from_user_id   = request.user.id,
                to_user_id     = to_user_id,
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        
        elif not message_number_id:
            if Message.objects.filter(Q(to_user_id = to_user_id)&Q(from_user_id = user.id)|Q(to_user_id = user.id)&Q(from_user_id = to_user_id)).exists():
                return JsonResponse({'message' : 'UNABLE_TO_CREATE_MESSAGE_NUMBER'}, status = 400)

            message_number = MessageNumber.objects.create()
            try:
                message = Message.objects.create(
                    message_number_id = message_number.id,
                    content        = content,
                    from_user_id   = request.user.id,
                    to_user_id     = to_user_id,
                )
                return JsonResponse({'message' : 'SUCCESS'}, status = 400)
            except IntegrityError:
                return JsonResponse({'message' : 'TO_USER_NOT_EXISTS'}, status = 400)        
         
        else:
            return JsonResponse({'message' : 'MESSAGE_NUMBER_NOT_MATCH_TO_USER'}, status = 400)
        
        playlist = data.get('playlist_id', None)
        song     = data.get('song_id', None)
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

        return JsonResponse({'message' : 'SUCCESS'}, status = 200)

    @login_required
    def get(self, request):
        try:
            user    = request.user.id
            message_number_id = request.GET.get('chatroom_id', None)
            with connection.cursor() as db_cursor:

                if message_number_id:
                    db_cursor.execute('''
                        select 
                        message_numbers.id as chatromm_id,
                        messages.id as message_id,
                        messages.content as content,
                        messages.created_at as created_at,
                        from_users.name as from_user_name,
                        from_users.profile_image as from_user_profile_image,
                        from_users.id as from_user_id,
                        to_users.name as to_user_name,
                        to_users.profile_image as to_user_profile_image,
                        to_users.id as to_user_id
                        from message_numbers
                        left join messages on messages.message_number_id = message_numbers.id 
                        left join users as from_users on messages.from_user_id = from_users.id 
                        left join users as to_users on messages.to_user_id = to_users.id 
                        where (from_user_id = %(user)s or to_user_id = %(user)s) and message_numbers.id = %(message_number_id)s
                        order by messages.created_at DESC
                    ''', {'message_number_id' : message_number_id, 'user' : user})
                    messages = db_cursor.fetchall()
                    messages = [{
                        'chatroom_id' : m[0], 
                        'message_id' : m[1],
                        'content' : m[2],
                        'created_at' : m[3],
                        'from_user_name' : m[4],
                        'from_user_profile_image' : m[5],
                        'from_user_id' : m[6],
                        'to_user_name' : m[7],
                        'to_user_profile_image' : m[8],
                        'to_user_id' : m[9],
                        'playlist_id' : Message.objects.valeus
                    } for m in messages]
                
                    return JsonResponse({'message_details' : messages}, status = 200)
            

                db_cursor.execute('''
                    select 
                    message_numbers.id as message_number,
                    (select content from messages where message_number_id = message_numbers.id order by created_at DESC LIMIT 1) as last_message_content,
                    (select created_at from messages where message_number_id = message_numbers.id order by created_at DESC LIMIT 1) as last_message_created_at,
                    (select id from messages where message_number_id = message_numbers.id order by created_at DESC LIMIT 1) as last_message_id,
                    (select is_checked from messages where message_number_id = message_numbers.id order by created_at DESC LIMIT 1) as last_message_is_checked,
                    (select from_user_id from messages where message_number_id = message_numbers.id order by created_at DESC LIMIT 1) as from_user_id,
                    (select to_user_id from messages where message_number_id = message_numbers.id order by created_at DESC LIMIT 1) as to_user_id,
                    (select users.name from messages left join users on messages.from_user_id = users.id where message_number_id = message_numbers.id order by messages.created_at DESC LIMIT 1) as from_user_name,
                    (select users.name from messages left join users on messages.to_user_id = users.id where message_number_id = message_numbers.id order by messages.created_at DESC LIMIT 1) as to_user_name,
                    (select users.profile_image from messages left join users on messages.to_user_id = users.id where message_number_id = message_numbers.id order by messages.created_at DESC LIMIT 1) as to_user_profile_image,
                    (select users.profile_image from messages left join users on messages.to_user_id = users.id where message_number_id = message_numbers.id order by messages.created_at DESC LIMIT 1) as from_user_profile_image
                    from message_numbers
                    left join messages on messages.message_number_id = message_numbers.id 
                    where messages.to_user_id = %(user_id)s
                    or messages.from_user_id = %(user_id)s
                    group by message_numbers.id 
                ''', {'user_id' : user})
                
                message_number_list = db_cursor.fetchall()
                message_number_list = [{
                    'chatroom_id': m[0], 
                    'content': m[1], 
                    'created_at': m[2], 
                    'message_id': m[3],
                    'is_checked' : m[4],
                    'from_user_id' : m[5],
                    'to_user_id' : m[6],
                    'from_user_name' : m[7],
                    'to_user_name' : m[8],
                    'to_user_profile_image' : m[9],
                    'from_user_profile_image' : m[10]
                } for m in message_number_list]
            return JsonResponse({'data' : message_number_list}, status = 200)

        except ValueError:
            return JsonResponse({'message' : 'UNAUTHORIZED_USER'}, status = 403)

class LatestMessageView(View):
    @login_required
    def get(self, request):
        user = request.user.id
        message_chunk = Message.objects.filter(Q(from_user_id = user)|Q(to_user_id = user))
        latest_message = message_chunk.order_by('created_at').last() 
        latest_message_chunk = (
                 Message.objects.prefetch_related('playlist', 'song')
                .filter((Q(from_user_id = latest_message.from_user_id)&Q(to_user_id = latest_message.to_user_id))|(Q(from_user_id = latest_message.to_user_id)&Q(to_user_id = latest_message.from_user_id)))
                .order_by('created_at')
        )
        latest_messages_details = [
                        {
            'message_id'     : message.id,
            'content'        : message.content,
            'from_user_id'   : message.from_user_id,
            'from_user_name' : message.from_user.name,
            'from_user_img'  : message.from_user.profile_image,
            'to_user_id'     : message.to_user_id,
            'to_user_name'   : message.to_user.name,
            'to_user_img'    : message.to_user.profile_image,
            'is_checked'     : message.is_checked,
            'created_at'     : message.created_at,
            'playlist'       : [{'playlist_id' : data.id, 'name' : data.name} for data in message.playlist.all()],
            'song'           : [{'song_id' : data.id, 'name' : data.name} for data in message.song.all()],
            } for message in latest_message_chunk
        ]

        return JsonResponse({'latest_message_details' : latest_messages_details}, status = 200)


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

        return JsonResponse({'following' : to_follow}, status = 200)

class UserRecommendationView(View):
    @login_required
    def get(self, request):
        user=request.user
        limit = request.GET.get('limit', 3)
        random_users = User.objects.prefetch_related('follow').order_by('?')
        recommended_user = [
            {'name'           : random_user.name,
            'id'              : random_user.id, 
            'song_count'      : random_user.song_set.count(), 
            'to_follow_count' : random_user.follow.values().count(),
            'profile_image'   : random_user.profile_image,
            'mutual_follow'   : True if Follow.objects.filter(from_follow_id = user.id, to_follow_id = random_user.id) else False} 
            for random_user in random_users[:limit]
        ]

        return JsonResponse({'data' : recommended_user}, status = 200)

class GoogleSignInView(View):
    def post(self, request):
        id_token     = request.headers.get('id_token', None)
        user_request = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
        user_info    = user_request.json()
        google_email = user_info.get('email')
        google_name  = user_info.get('name')
        print(id_token)
        if User.objects.filter(email = google_email).exists():
            user       = User.objects.get(email = google_email)
            token      = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)
            return_key = {'user' : {'token' : token.decode('utf-8'), 'uuid' : user.uuid}}
            print(return_key)
            return JsonResponse(return_key, status = 200)

        user = User.objects.create(
            email = google_email,
            name  = google_name,
            uuid  = str(uuid.uuid3(uuid.NAMESPACE_DNS, google_email).hex)
        )
        token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)
        user_uuid  = user.uuid
        return_key = {'user' : {'token' : token.decode('utf-8'), 'uuid' : user_uuid}}
        print(return_key)

        return JsonResponse(return_key, status = 200)

class NotificationView(View):
    @login_required
    def get(self, request):
        user = request.user.id
        message_checked = (
                Message.objects
                .filter(to_user_id = user)
                .order_by('created_at')
                .last().is_checked
        )
        from_user_id    = (
                Message.objects
                .filter(to_user_id = user)
                .order_by('created_at')
                .last().from_user_id
        )
        follow_checked  = (
                Follow.objects
                .filter(to_follow = user)
                .order_by('created_at')
                .last().is_checked
        )
        from_follow_id  = (
                Follow.objects
                .filter(to_follow = user)
                .order_by('created_at')
                .last().from_follow_id
        )
        
        if not message_checked  or not follow_checked:
            return_key = {
                    'data' : {
                        'message_checked' : message_checked, 
                        'follow_checked'  : follow_checked,
                        'follower_id'     : from_follow_id,
                        'sender'          : from_user_id,
                    }
            }
            return JsonResponse(return_key, status = 200)
        
        return_key = {
                'data' : {
                    'message_checked' : message_checked, 
                    'follow_checked'  : follow_checked,
                }
        }
        return JsonResponse(return_key, status = 200)

class StatusView(View):
    @login_required
    def get(self, request):
        user = request.user.id
        follow_status  = (
                Follow.objects
                .filter(to_follow_id = user, is_checked = False)
                .select_related('from_follow', 'to_follow')
                .order_by('created_at')
        )
        if not len(list(follow_status)):
            return JsonResponse({'message' : 'EMPTY_UPDATES'}, status = 400)
        
        return_key = {
            'data' : 
                [{'follower_name'             : status.from_follow.name,
                    'follower_id'             : status.from_follow.id,
                    'follower_follower_count' : status.from_follow.follow_reverse.all().count(), 
                    'follower_song_count'     : status.from_follow.song_set.all().count(),
                    'follower_image'          : status.from_follow.profile_image,
                    'follow_at'               : status.created_at,
                    'is_checked'              : status.is_checked,
                    'mutual_follow'           : True if Follow.objects.filter(from_follow_id = user, to_follow_id = status.from_follow_id) else False} 
                    for status in follow_status]
        }
        Follow.objects.filter(to_follow_id = user).update(is_checked = True)

        return JsonResponse(return_key, status=200)

class UserInfoView(View):
    @login_required
    def get(self, request):
        user = request.user
        return JsonResponse({
            'data' : {'user_id'  : user.id, 
                    'user_name'  : user.name, 
                    'user_image' : user.profile_image}
            })
