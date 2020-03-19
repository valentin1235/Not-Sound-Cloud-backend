
file_path='superbee.mp3'
 # file_path='background.wav'

from pydub       import AudioSegment
from pydub.utils import mediainfo
audio = AudioSegment.from_file(file_path)
audio.set_channels(1)
# sampling_rate = audio.frame_rate*4


source = 'superbee.mp3'

f = open(source,'rb+')
w = open('w.txt','wb+')
print(audio._data)
# while True:
#     c=audio.raw_data
#     if c:
#         print(c)
#     else :
#         break    
# w.write(f.read())














# sum=0
# count = 0
# arr=[]
# print(max(audio.raw_data))
# for element in audio.raw_data:
#     count+=1
#     # sum+=abs(element)
#     sum+=element
#     if(count>sampling_rate):
#         data =((sum)/sampling_rate)
#         arr.append(int(data))
#         sum=0
#         count=0

 # plt.plot(arr)
 # plt.show()

# print(arr)
# print(len(arr))





#import librosa
#import matplotlib.pyplot as plt
#import numpy as np
#import math
#file_path='background.wav'
#
#audio, sampling_rate = librosa.load(file_path,mono=True)
#durations_of_sound = len(audio)/sampling_rate#노래 길이
#sum=0
#blocks=270
#count = 0
#arr=[]
#one_block_data=int(len(audio)/270)
#for element in audio:
#    count+=1
#    sum+=abs(element)
#
#    if(count>=one_block_data):
#        arr.append(int(round(((sum)/one_block_data),3)*300))
#        sum=0
#        count=0
#
#print(arr)
#print(len(arr))
#plt.plot(arr)
#plt.show()
#[0, 0, 0, 0, 0, 14, 17, 32, 8, 15, 63, 50, 11, 47, 57, 51, 20, 45, 62, 60, 52, 45, 39, 34, 24, 26, 33, 34, 28, 31, 32, 36, 32, 34, 30, 39, 30, 35, 32, 44, 43, 24, 40, 55, 51, 33, 51, 54, 49, 22, 49, 67, 58, 47, 57, 60, 38, 20, 23, 54, 62, 33, 45, 52, 57, 46, 42, 56, 60, 64, 43, 16, 33, 22, 24, 29, 32, 24, 24, 33, 27, 27, 30, 28, 30, 33, 28, 40, 33, 58, 35, 51, 62, 57, 40, 55, 63, 64, 43, 50, 59, 71, 64, 58, 51, 68, 20, 22, 30, 31, 25, 30, 30, 36, 30, 36, 30, 32, 32, 31, 36, 34, 51, 41, 51, 52, 49, 53, 44, 53, 51, 37, 59, 58, 54, 47, 46, 51, 42, 37, 30, 42, 47, 23, 29, 36, 48, 40, 33, 43, 48, 48, 38, 30, 25, 24, 23, 28, 32, 24, 27, 37, 32, 36, 38, 37, 36, 40, 35, 43, 33, 53, 37, 50, 62, 58, 53, 56, 63, 66, 45, 48, 60, 73, 64, 60, 58, 70, 31, 34, 34, 31, 32, 33, 37, 45, 42, 32, 30, 28, 36, 27, 24, 36, 45, 40, 46, 60, 60, 53, 48, 58, 48, 37, 47, 68, 60, 48, 51, 58, 35, 36, 33, 42, 46, 39, 31, 44, 41, 43, 29, 42, 48, 43, 43, 32, 45, 53, 42, 51, 57, 54, 48, 52, 61, 62, 40, 53, 66, 63, 60, 51, 64, 35, 0, 0, 0, 0]
#
