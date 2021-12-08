import argparse
import requests
import shutil
import pickle
import os
import sys
from sub_term import Vod
from sub_term import THUMBNAILS
from sub_term import get_video

path = os.path.dirname(sys.argv[0])

parser = argparse.ArgumentParser()
parser.add_argument('--profile', '-p', type=str, default='def')
parser.add_argument('--video', '-v', type=str)
args = parser.parse_args()

s = args.video[-11:]

with open(path+'/'+args.profile+'/' + s, 'rb') as v:
    vid = pickle.load(v)

# create cache directory for thumbnails
if ((not os.path.exists(path+'/cache')) and THUMBNAILS):
    os.makedirs(path+'/cache')

if(THUMBNAILS and os.path.exists(path+'/cache/'+s+'.jpg') == False):
    image_url = "https://img.youtube.com/vi/" + s + "/0.jpg"
    filename = path+'/cache/' + image_url.split("/")[-2] + '.jpg'

    r = requests.get(image_url, stream=True)
    r.raw.decode_content = True

    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

print("\033[1;31m" + vid.title + "\033[0m" +
      '\n\033[;34m' + vid.channel + '\033[0m' +
      '\n' + vid.views + ' views'+" "*(15-len(vid.views)), end=" ")
try:
    if(round(vid.likes, 2) < 80):
        print('\033[7;31m'+str(round(vid.likes, 2))+'%\033[0m\t' + vid.upload)
    elif(round(vid.likes, 2) < 95):
        print('\033[1;33m'+str(round(vid.likes, 2))+'%\033[0m\t' + vid.upload)
    else:
        print('\033[;32m'+str(round(vid.likes, 2))+'%\033[0m\t' + vid.upload)
except AttributeError as a:
    print('could not get likes')

print('\033[4;37m' + get_video(vid.videoid) +
      '\033[0m\n')
try:
    print(vid.description)
except AttributeError as a:
    print('could not get description')

if(THUMBNAILS):
    os.system('viu -w 60 "' + path + '/cache/' + s + '.jpg"')

# print(climage.convert('./cache/' + s + '.jpg'))
"""
with ueberzug.Canvas() as c:
        with c.lazy_drawing:
                demo = c.create_placement(
                    'demo', x=0, y=0, scaler=ueberzug.ScalerOption.COVER.value)
                demo.path = '/home/ben/Public/xps/cache/' + s + '.jpg'
                demo.y = 5
                demo.visibility = ueberzug.Visibility.VISIBLE

"""
