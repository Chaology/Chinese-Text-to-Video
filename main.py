import imageio
from io import StringIO
import os
import sys, getopt
import shutil
import cv2
import re
import string
import numpy as np

from moviepy.editor import *
from gtts import gTTS

import gensim
from gensim import corpora

import download_image as image_downloader
from get_keyword import get_word_from_sentence
from util import format_text
from pdf_to_txt import pdf_2_txt


audio_dir = './audio/tmp'
picture_dir = './picture/tmp'
video_dir = './video/tmp'
if os.path.exists(audio_dir):
    shutil.rmtree(audio_dir)
if os.path.exists(picture_dir):
    shutil.rmtree(picture_dir)
if os.path.exists(video_dir):
    shutil.rmtree(video_dir)


# pdf_2_txt("sample.pdf","txt/sample.txt")


count_lines = 1
_FPS=24

fr = open('txt/sample.txt')
text = ''.join(fr.readlines())
sentences = text.split('。')
for sentence in sentences[:-1]:
    all_topics = get_word_from_sentence(sentence)
    print ('\n\n',sentence,'\n')
    print ("all topics ", all_topics, '\n\n')
    folder_names = []
    for i in range(0,len(all_topics)):
        if len(all_topics) > 4:
            image_downloader.download_images(all_topics[i],1)
        else:
            image_downloader.download_images(all_topics[i],2)
        folder_names.append(all_topics[i].replace(' ','_'))

    text_sentences=[f for f in sentence.split('，') if len(f)>1]
    if len(text_sentences) <=0:
        continue

    if not os.path.exists(audio_dir):
        os.mkdir(audio_dir)
    if not os.path.exists(picture_dir):
        os.mkdir(picture_dir)
    if not os.path.exists(video_dir):
        os.mkdir(video_dir)

    print ("creating "+str(len(text_sentences))+" audio files ")

    for i in range(0,len(text_sentences)):
        tts = gTTS(text=text_sentences[i], lang='zh', slow=False)
        tts.save(audio_dir+'/'+str(i)+'.mp3')
        print ('\n',text_sentences[i],'\n')
        print ("created "+ str(i)+ " audio file")

    text_clip_list=[]
    audio_clip_list=[]
    silence = AudioFileClip('./audio/silence.mp3').subclip(0,0.1)
    audio_clip_list.append(silence)


    for i in range(0,len(text_sentences)):
        sent_audio_clip=AudioFileClip(audio_dir+'/'+str(i)+'.mp3')
        print ("length of audio: "+str(i)+" = ",sent_audio_clip.duration)
        audio_clip_list.append(sent_audio_clip)
        sent_txt_clip = TextClip(format_text(text_sentences[i]),font='ArialUnicode',fontsize=150,color='yellow',bg_color='black',stroke_width=30).set_pos('bottom').set_duration(sent_audio_clip.duration).resize(width=1000)
        text_clip_list.append(sent_txt_clip)

    audio_clip=concatenate_audioclips(audio_clip_list)
    
    file_names = []
    for i in range(0,len(folder_names)):
        files = (fn for fn in os.listdir(picture_dir+'/'+folder_names[i]) if fn.endswith('.jpg') or fn.endswith('.png') or fn.endswith('.PNG') or fn.endswith('.JPG') or fn.endswith('.jpeg') or fn.endswith('.JPEG'))
        for file in files:
            file_names.append(folder_names[i]+'/'+file)

    s_file_names = file_names
    number_of_images=len(s_file_names)
    print (s_file_names)


    video_clip_list=[]
    black_clip=ImageClip('./picture/black1.jpg').set_duration(0.1).set_fps(_FPS)
    video_clip_list.append(black_clip)
    black = './picture/black1.jpg'
    title_clip_list = []
    if number_of_images > 0:
        for f in s_file_names:
            print (f)
            temp_clip=ImageClip(picture_dir+'/'+f).set_duration(audio_clip.duration/number_of_images).set_position('center').set_fps(_FPS).crossfadein(0.5)
            name_txt_clip = TextClip(format_text(' '.join([word[:1].upper()+word[1:] for word in f.split('/')[0].split('_')])),font='ArialUnicode',fontsize=150,color='yellow',bg_color='black',stroke_width=30).set_position('top').set_duration(audio_clip.duration/number_of_images).resize(height=30)
            title_clip_list.append(name_txt_clip)
            video_clip_list.append(temp_clip)
            print ('temp_clip width: ',temp_clip.size)
    else:
        temp_clip=ImageClip(black).set_duration(audio_clip.duration).set_fps(_FPS)
        video_clip_list.append(temp_clip)

    if len(video_clip_list) > 0:
        video_clip = concatenate_videoclips(video_clip_list).set_position('center')
    
    if len(text_clip_list) > 0:
        txt_clip=concatenate_videoclips(text_clip_list).set_position('bottom')

    if len(title_clip_list) > 0:
        title_clip = concatenate_videoclips(title_clip_list).set_position('top')
        result=CompositeVideoClip([video_clip,txt_clip,title_clip])
    else:
        result=CompositeVideoClip([video_clip,txt_clip])

    print ("Composite video clip size: ",result.size)

    result_with_audio=result.set_audio(audio_clip)


    print ("audio duration: "+str(audio_clip.duration))
    print ("result duration: "+str(result.duration))
    print ("result audio duration: "+str(result_with_audio.duration))


    result_with_audio.write_videofile(video_dir+'/'+str(count_lines)+'.mp4',codec='libx264',fps=_FPS)
    count_lines += 1

    shutil.rmtree(audio_dir)
    shutil.rmtree(picture_dir)


fr.close()

video_files = [fn for fn in os.listdir(video_dir) if fn.endswith('.mp4')]
video_files = sorted(video_files, key=lambda x: int(x.split('.')[0]))
video_clip_list = []
for video in video_files:
    clip = VideoFileClip(video_dir+'/'+video).crossfadein(0.5)
    video_clip_list.append(clip)

video_clip = concatenate_videoclips(video_clip_list)
video_clip.write_videofile('sample.mp4',codec='libx264',fps=_FPS)