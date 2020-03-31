from django.views           import View
from django.http            import HttpResponse, JsonResponse
from .models                import Song,Tag,TagPlaylist,TagSong
from user.models            import User
from user.utils             import login_required
from django.conf            import settings
from user.utils             import login_required
from pydub                  import AudioSegment
from pydub.utils            import make_chunks

from pydub.silence import split_on_silence
import os
import re
import  numpy as np
import mimetypes
import librosa
import json


from django.http.response import StreamingHttpResponse

class SongView(View):
    def get(self,request,song_id,option):
        try:
            if option == 'play':
                songs_detail = self.getAudioInfo(Song.objects.filter(id=song_id))
            elif option == 'home':
                songs_detail = self.showHomeAudioInfo(Tag.objects.filter(is_popular=True))
            elif option == 'streams':
                songs_detail = self.streamAudioInfo(Song.objects,song_id)
                 
            return JsonResponse({'song':songs_detail},status=200)

        except Exception as idf:
            return JsonResponse({"message":idf},status=400) 
    
    def getAudioInfo(self,songs):
        get_song     = songs.get()
        songs_detail = [{
            'song_id'       : get_song.id,
            'song_name'     : get_song.name,
            'song_path'     : get_song.song_url,
            'artist_name'   : get_song.user.name,
            'artist_img'    : get_song.user.profile_image,
            'sample_rate'   : get_song.song_sample_rate,
            'small_img_url' : get_song.small_image,
            'big_img_url'   : get_song.big_image,
            'song_tag'      : [tags.name for tags in get_song.tag_set.all()],
            'wave_data'     : self.getWaveData(get_song.id)
        }]
        return songs_detail
    def streamAudioInfo(self,songs,current_page):
        load_page=10
        current_page=int(current_page)
        songs=songs.order_by('-id')[current_page:current_page+10]
        songs_detail = [{
            'song_id'       : get_song.id,
            'song_name'     : get_song.name,
            'song_path'     : get_song.song_url,
            'artist_name'   : get_song.user.name,
            'artist_img'    : get_song.user.profile_image,
            'sample_rate'   : get_song.song_sample_rate,
            'small_img_url' : get_song.small_image,
            'big_img_url'   : get_song.big_image,
            'song_tag'      : [tags.name for tags in get_song.tag_set.all()],
            'wave_data'     : self.getWaveData(get_song.id)
        }for get_song in songs]
        
        return songs_detail
    def showHomeAudioInfo(self,tags):
        get_tag = tags
        info    = [{
            tag.name:[{
            'song_id'       :   detail.id,
            'song_name'     :   detail.name,
            'sample_rate'   :   detail.song_sample_rate,
            'song_path'     :   detail.song_url,
            'small_img_url' :   detail.small_image,
            'big_img_url'   :   detail.big_image,
            'artist_name'   :   detail.user.name
            }for detail in tag.song.order_by('-id')[:10]]
         }for tag in get_tag]
        return info

    def getWaveData(self,song_id):
        path=settings.MEDIA_URL+"{}.txt".format(song_id)
        r = open(path,'r+')
        arr=[]
        while True:
            data= r.readline()
            if data:
                arr.append(int(data))
            else :
                break
        return arr     

class SongUploadView(View):

    @login_required
    def post(self,request):
        try:
            user_id     = request.user.id
            data    = json.loads(request.body)
            obj,flag=Tag.objects.get_or_create(name=data['tag_name'])
            file        = request.FILES['file']
            sample_rate = self.upload_file(file,user_id)
            song_obj    = Song.objects
            return HttpResponse(status=200)
        except Exception as identifier:
            print(identifier)
            return HttpResponse(status=400)



    def upload_file(self,f,user_id):
        path=settings.MEDIA_URL+"{}".format(user_id)
        with open(path+".mp3",'wb+') as destination:
            for chunk in f.chunks():
               destination.write(chunk)
        self.audio_analysis(path,user_id)


    def audio_analysis(self,path,user_id):
        audio, sampling_rate = librosa.load(path,mono=True)
        sum = 0
        count = 0 
        arr = []
        blocks = 270
        one_block_data = int(len(audio)/blocks)
        w = open(path+".txt",'w')
        for element in audio:
            count+=1
            sum+=abs(element)    
            if(count>=one_block_data):
                data = int(round(((sum)/one_block_data),3)*300)
                arr.append(data)
                count = 0
                sum = 0
                w.write(str(data)+"\n")
        print(arr)
        w.close()
        return sampling_rate

class playView(View):

    def __init__(self):
        self.total_len = 0

    def get(self,request,song_id,seconds):
        try:
            self.total_len=0
            source = settings.MEDIA_URL+"{}.mp3".format(song_id)
            # print("file size=", end=""), print(os.path.getsize(source))
            size = os.path.getsize(source)
            audio=AudioSegment.from_file(source)
            durations=int(len(audio)/1000)
            # raw_size= audio.raw_size
            # print(durations)
            size_per_sec = size/durations
            # sr     = Song.objects.filter(id=song_id).get().song_sample_rate
            resp   = StreamingHttpResponse(self.iteration(source,size_per_sec*seconds),status=200, content_type='audio/mp3')            
            resp['Cache-Control']='no-cache'
            resp['Accept-Ranges']='bytes'
            self.total_len=os.path.getsize(source)
            return resp
        except Exception as identifier:
            print(identifier)
            return HttpResponse(status=400)

    def iteration(self,source,times):# 처리해주는 놈
        f = open(source,'rb+')
        f.seek(int(times))
        while True: 
            c = f.read(512)
            if c:
                yield c
            else:
                break


class Test(View):

    def __init__(self):
        self.total_len = 0

    def get(self,request):
        try:
            self.total_len=0
            song_id=2
            source = settings.MEDIA_URL+"{}.mp3".format(song_id)
            size = os.path.getsize(source)
            audio=AudioSegment.from_file(source)
            durations=int(len(audio)/1000)
            # raw_size= audio.raw_size
            # print(durations)
            # size_per_sec = size/durations
            size = int(len(audio.raw_data)/1024)
            f = open('tet','wb+')
            for element in audio.raw_data:
                f.write(element)

            for i in range(size):
                source[i*1024:(i+1)*1024]
            print(size)
            resp   = StreamingHttpResponse(self.iteration('test'),status=200, content_type='audio/mp3')
            print(audio.raw_data[0])
            resp['Cache-Control']='no-cache'
            return resp
        except Exception as identifier:
            print(identifier)
            return HttpResponse(status=400)
        return HttpResponse(status=200)

    def iteration(self,source):# 처리해주는 놈
        f =open('tet','rb+')

        while True:
            c=f.read(1024)
            if c:
                yield c
            else:
                break    
        # size = int(len(source)/1024)
        # i=0
        # for i in range(size):
        #    yield source[i*1024:(i+1)*1024]
        # f = open(source,'rb+')
        # # f = source.chunks()
        # # f.seek(61*int(chunks))
        # # with open(source,'rb') as f:
        # while True: 
        #     c = f.read(512)
        #     if c:
        #         yield c
        #     else:
        #         break