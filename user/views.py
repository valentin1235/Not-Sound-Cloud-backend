import jwt, bcrypt, json, uuid

from django.db        import IntegrityError
from django.db.models import Count, Q
from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db    import IntegrityError

from .models                    import User, Message, Follow
from music.models               import Song, Playlist

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            User.objects.create(
                    email         = data['email'],
                    password      = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    age           = data['age'],
                    name          = data['name'],
                    sex           = data['sex'],
                    profile_image = data['profile_image'],
                    uuid          = str(uuid.uuid3(uuid.NAMESPACE_DNS, data['email']).hex)
            )
            
            return HttpResponse(status = 200)

        except KeyError:
            
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

        except IntegrityError:
            
            return JsonResponse({'message' : 'USER_EXISTS'}, status = 400)
