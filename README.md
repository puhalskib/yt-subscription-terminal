# YT Subscription Terminal
A youtube subscription rss feed fetch.

I don't wanna use youtube because I'm addicted and [ytfzf](https://github.com/pystardust/ytfzf) doesn't work for my 900 subscriptions

![usage](https://github.com/puhalskib/yt-subscription-terminal/blob/master/shot1.jpg)

![fzf view](https://github.com/puhalskib/yt-subscription-terminal/blob/master/shot2.jpg)

## Installation
```
pip install feedparser pyfzf progressbar progressbar2
git clone https://github.com/puhalskib/yt-subscription-terminal
```
## Dependecies
- [fzf](https://github.com/junegunn/fzf)
- [mpv](https://mpv.io/)
- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- python3.something

all must be available to the path

## Usage

- gather subscriptions using [google takeout](https://takeout.google.com/)
- channels must be in the form "https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID_HERE"
- for example: https://www.youtube.com/feeds/videos.xml?channel_id=UCsrdm4f-MU1mEZbcXwqDjLg
- put links in a urls.txt file in the same folder as the script and seperate them with a new line

```
python3 main.py
```
```
usage: main.py [-h] [--format FORMAT] [--load]

Fetch youtube subscription and watch videos

optional arguments:
  -h, --help            show this help message and exit
  --format FORMAT, -f FORMAT
                        look for specified format (default: 720)
  --load, -l            load from saved subscription videos (no fetching)
```

## Config

If you wan't to change the number of threads the script uses to get better performance, change the THREADNUM variable at the top of the script (defaut 15). For the number of videos gathered per channel change CHANNEL_VIDEO_NUM (defaut 4).

## TODO

- add audio only
- add format selector on video (like fzf)
- add thumbnail viewer
