import feedparser
from threading import Thread
from progressbar import progressbar
import math
import pickle
from pyfzf.pyfzf import FzfPrompt
import os
import argparse

THREADNUM = 15
CHANNEL_VIDEO_NUM = 4

class Vod:
    def __init__(self, entrie):
        self.views = entrie.media_statistics['views']
        self.title = entrie.title
        self.channel = entrie.author
        self.videoid = entrie.yt_videoid
        self.published = entrie.published
        self.thumbnail = entrie.media_thumbnail[0]['url']


def get_video(s: str):
    return ("https://www.youtube.com/watch?v=" + s)

#
# get command arguments
#


parser = argparse.ArgumentParser(
    description='Fetch youtube subscription and watch videos')
parser.add_argument('--format', '-f', type=int, default='720',
                    help='look for specified format (default: 720)')
parser.add_argument('--load', '-l', action='store_true',
                    help='load from saved subscription videos (no fetching)')
args = parser.parse_args()

#
# Fetch youtube videos
#

vods = []
if args.load == False:
    url_array = []
    with open('urls.txt') as url_file:
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

    #
    # Save videos to file
    #
    outfile = open('subs', 'wb')
    pickle.dump(vods, outfile)
    outfile.close()

else:
    #
    # Load videos from file
    #
    infile = open('subs', 'rb')
    vods = pickle.load(infile)
    infile.close

#
# choose a video from the subscription videos
#

sub_vods = []
for z in vods:
    sub_vods.append(z.title + ' - ' + z.videoid)
fzf = FzfPrompt()
chosen = fzf.prompt(sub_vods)
chosen = chosen[0]
chosen = chosen[-11:]
print('playing ', chosen)

#
# Play video
#

os.system('mpv "--ytdl-format=best[height<=?' +
          str(args.format) + ']" ' + get_video(chosen))
