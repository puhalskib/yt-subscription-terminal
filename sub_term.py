#!/usr/bin/env python3

import feedparser
from threading import Thread
from progressbar import progressbar
import math
import pickle
from pyfzf.pyfzf import FzfPrompt
import os
import argparse
import sys


def get_month(m):
    switch = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }
    return switch.get(m)


class Vod:
    def __init__(self, entry):
        self.views = entry.media_statistics['views']
        self.title = entry.title
        self.channel = entry.author
        self.videoid = entry.yt_videoid
        self.upload = f"{get_month(entry.published_parsed.tm_mon)} {entry.published_parsed.tm_mday}, {entry.published_parsed.tm_year}"
        self.description = entry.summary
        self.likes = float(entry.media_starrating['average']) * 20
        self.published = entry.published


THREADNUM = 12
CHANNEL_VIDEO_NUM = 15
THUMBNAILS = False


def get_video(s: str):
    return ("https://www.youtube.com/watch?v=" + s)

#
# get command arguments
#


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Fetch youtube subscription and watch videos')
    parser.add_argument('--format', '-f', type=int, default='720',
                        help='look for specified format (default: 720)')
    parser.add_argument('--load', '-l', action='store_true',
                        help='load from saved subscription videos (no fetching)')
    parser.add_argument('--profile', '-p', type=str, default='def',
            help='fetch videos only from a certain profile (default: def)')
    args = parser.parse_args()
    
    #catch error
    if (args.profile == 'cache' or args.profile == ''):
        raise Exception('Invalid profile name')

    

    #
    # Fetch youtube videos
    #
    path = os.path.dirname(sys.argv[0])

    if(path == ""):
        path = "./"


    vods = []
    if args.load == False:
        url_array = []
        with open(path+'/'+args.profile+'.txt') as url_file:
            url_array = url_file.read().splitlines()

        # split the array into arrays of 100 length each
        urls_split = [url_array[i:i+math.ceil(len(url_array)/THREADNUM)]
                      for i in range(0, len(url_array), math.ceil(len(url_array)/THREADNUM))]

        def parse_section(url_section):
            for x in progressbar(url_section):
                d = feedparser.parse(x)
                try:
                    for y in range(CHANNEL_VIDEO_NUM):
                        v1 = Vod(d.entries[y])
                        vods.append(v1)
                except IndexError as e:
                    pass

        print('starting ', THREADNUM, ' threads...\nfetching from youtube...')
        threads = []
        for n in urls_split:
            t = Thread(target=parse_section, args=(n,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        def getTime(e):
            return e.published

        print('sorting...')
        vods.sort(reverse=True, key=getTime)

        # check if sub cache exists
        if not os.path.exists(path+'/'+args.profile):
            os.makedirs(path+'/'+args.profile)

        # clear sub cache
        os.system('rm -rf ' + path + '/'+args.profile+'/*')

        #
        # Save videos to files
        #
        for z in vods:
            with open(path+'/'+args.profile+'/'+z.videoid, 'wb') as f:
                pickle.dump(z, f)

    else:
        #
        # Load videos from files
        #
        for filename in os.listdir(path+'/'+args.profile):
            with open(path+'/'+args.profile+'/'+filename, 'rb') as f:
                vods.append(pickle.load(f))

        def getTime(e):
            return e.published

        print('sorting...')
        vods.sort(reverse=True, key=getTime)

    #
    # choose a video from the subscription videos
    #

    sub_vods = []
    for z in vods:
        sub_vods.append(z.channel + " "*(21-len(z.channel)) +
                        '- ' + z.title + " "*(56-len(z.title)) + '--- ' + z.videoid)

    # if new videos, clear thumbnail cache
    if(args.load == False):
        os.system('rm -rf ' + path + '/cache/*.jpg')

    fzf = FzfPrompt()
    chosen = fzf.prompt(
        sub_vods, '--preview "python3 ' + path + '/preview.py -p '+args.profile+' -v {}" --preview-window="left:40%:noborder:wrap"')
    chosen = chosen[0]
    chosen = chosen[-11:]
    print('Opening Player: https://www.youtube.com/watch?v=' + chosen)

    #
    # Play video
    #

    os.system('mpv "--ytdl-format=bestvideo[height<=?' +
              str(args.format) + '][vcodec!=?vp9]+bestaudio/best" ' + get_video(chosen))
