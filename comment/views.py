import json

from django.views           import View
from django.http            import HttpResponse, JsonResponse

from user.utils                import login_required
from .models                   import Comment
from user.models               import User, Message, Follow, MessagePlaylist, MessageSong, GoogleAccount
from song.models               import Song, Playlist
from notsoundcloud.my_settings import SECRET_KEY, ALGORITHM

class CommentView(View):
    @login_required
    def post(self, request, song):
        try:
            data = json.loads(request.body)
            user = request.user.id
            Comment.objects.create(
                user_id = user,
                song_id = song,
                content = data['content'],
                position = data['position'],
            )
        
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'})

    @login_required
    def get(self, request, song):
        comments     = Comment.objects.select_related('user').filter(song_id = song)
        comment_info = [{
            'created_at' : comment.created_at, 
            'user_name'  : comment.user.name, 
            'content'    : comment.content, 
            'position'   : comment.position,
            'song_id'    : song,}
            for comment in comments]
        
        return JsonResponse({
            'data' : 
            {'comment_info' : comment_info, 
            'comment_count' : comments.count()}}, 
            status = 200)
