import json, jwt

from .models import User
from notsoundcloud.my_settings import SECRET_KEY, ALGORITHM
# from jwt.exceptions            import InvalidTokenError

from django.http import JsonResponse, HttpResponse

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
        
        if not access_token:
            return JsonResponse({'message' : 'LOGIN_REQUIRED'}, status = 400)    
        
        try:
            decode = jwt.decode(access_token, SECRET_KEY, algorithm = ALGORITHM)
            user = User.objects.get(id=decode['user_id'])    
            request.user = user

        except InvalidSignatureError:
            JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)
            
        return func(self, request, *args, **kwargs)
            
    return wrapper
