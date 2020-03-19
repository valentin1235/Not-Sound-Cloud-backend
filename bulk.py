import os
import django
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE','notsoundcloud.settings')
django.setup()
from song.models import *
from user.models import *
import librosa

# f = open('sc.csv','r',encoding='utf-8')


# Tag.objects.create(name='Chill',is_popular=True)
# Tag.objects.create(name='WeWork',is_popular=True)
# Tag.objects.create(name='GracefulRain',is_popular=True)
# Tag.objects.create(name='WeWorkout',is_popular=True)
# Tag.objects.create(name='Wecode',is_popular=True)
# Tag.objects.create(name='Im SoundKloud',is_popular=False)
# Tag.objects.create(name='I love Te+Sla',is_popular=False)
# Tag.objects.create(name='Im Dev Dat',is_popular=False)

# count=1
# for element in range(1,31):
#     TagSong.objects.create()
#     TagSong.objects.filter(id=element+1).update(song_id=element,tag_id=count)
#     count+=1
#     if(count>=8):
#         count=1


# count=1

# rdr = csv.reader(f)
# i = 0
# for row in rdr:
#     if i>1:    
#         song_small_img  = row[1] 
        
#         song_big_img    = row[2]
        
#         song_name       = row[3]
        
#         csv_user_name   = row[4]
        
#         csv_user_email  = row[6]
        
#         csv_user_pw     = row[7]
        
#         csv_user_age    = row[8]
        
#         csv_user_gender = row[9]
        
#         csv_user_img    = 'http://bitly.kr/Tg79JWhg'
        
#         csv_song_desc   = row[12]


        
#         User.objects.create(email=csv_user_email,password=csv_user_pw,name=csv_user_name,gender=csv_user_gender,profile_image=csv_user_img)
        
#         Song.objects.create(name=song_name,description=csv_song_desc,small_image=song_small_img,big_image=song_big_img,song_url="{}".format(count)+".mp3")
        
#         count+=1
#     else:
#         i+=1
# def audio_analysis(element):
#         audio, sampling_rate = librosa.load('media/{}.mp3'.format(element),mono=True)
#         sum = 0
#         count = 0 
#         arr = []
#         blocks = 270
#         one_block_data = int(len(audio)/blocks)
#         w = open('media/{}.txt'.format(element),'w')
#         for element in audio:
#             count+=1
#             sum+=abs(element)    
#             if(count>=one_block_data):
#                 data = int(round(((sum)/one_block_data),3)*300)
#                 arr.append(data)
#                 count = 0
#                 sum = 0
#                 w.write(str(data)+"\n")
#         w.close()
#         return sampling_rate


# for element in range(1,32):    
#     samplerate=audio_analysis(element)
#     Song.objects.filter(id=element).update(song_sample_rate=samplerate,user_id=element)


# for element in range(1,32):
#     Song.objects.filter(id=element).update(song_url="{}.mp3".format(element))
arr=[
    {
    'name':'EunjiB',
    'img':'http://bitly.kr/Px8h1M8j'
    },
    {    
    'name':'WaguWagu',
    'img':'http://bitly.kr/LAXMdP6N'
    },
    {
    'name':'McYou',
    'img':'http://bitly.kr/14uVjAhU'
    },
    {
    'name':'Piguretto',
    'img':'http://bitly.kr/0MdZst81'
    },
    {
    'name':'Dev-Hong',
    'img':'http://bitly.kr/BzQ4R2eVo'
    },
    {
    'name':'1hr',
    'img':'http://bitly.kr/9XefTbSg'
    },
    {
    'name':'SUNSET',
    'img':'http://bitly.kr/mGnc4Juo'
    },
    {
    'name':'Ulfrid',
    'img':'http://bitly.kr/b8IU7EPr'
    },
    {
    'name':'GodRampart',
    'img':'http://bitly.kr/jwv8JCqf'
    },

    {
    'name':'HandKing',
    'img':'http://bitly.kr/vd7SyAO5'
    },

    {
    'name':'JoonsiK',
    'img':'http://bitly.kr/X8EceLpS'
    },
    {
    'name':'LightofBackend',
    'img':'http://bitly.kr/fQjkf34Q'
    },
    {
    'name':'DavDat',
    'img':'http://bitly.kr/BUVknI8z'
    }
]

count=1
for element in arr:
    User.objects.filter(id=count).update(name=element['name'],profile_image=element['img'])
    count+=1