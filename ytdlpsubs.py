#/usr/bin/python3
# ytdlpsubs.py

import os
import glob
import logging
import time
import re
import csv
import json
import sys

import yt_dlp
import pandas as pd

# Download YouTube subtitles into .sub file
def getSubtitles(link, lang, path):

    path = path + '/'
    write_sub = False
    ydl_opts = {}
    vid_title = ''
    err = 0

    # Figure out if there are manual or auto subtitles
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            vid_id = info['id']
            vid_title = info['title']
            if info['subtitles']:
                if lang in info['subtitles'].keys():
                    write_sub = True
    except:
        logging.warning("Could not extract video metadata.")
        err = 1

    # Auto subs vs. manual subs
    if write_sub is True:
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'subtitlesformat': 'json3',
            'subtitle': '--write-sub --sub-lang en',
        }

    else:
        ydl_opts = {
            'skip_download': True,
            'writeautomaticsub': True,
            'subtitlesformat': 'json3',
            'subtitle': '--write-sub --sub-lang en',
        }

    # Download subs
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(link)
            
            # rename and move to directory
            sub_file = glob.glob('*' + vid_id + '*')
            os.rename(sub_file[0], path + vid_id + ".sub")
    except:
        logging.warning("Could not extract subtitles from video.")
        err = 1

    return vid_title, err

# Get list of Video IDs from a playlist link
def getVideoIDs(playlist):

    ID_list = []
    err = 0

    ydl_opts = {
        'extract_flat': 'in_playlist',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist, download=False)
            ID_list = [d['id'] for d in info['entries']]
    
    except:
       logging.warning("Could not extract video IDs from playlist.")
       err = 1

    return ID_list

# Convert .sub files into usable .csv and .json
def convert_ytdlp_subs(ID, path):

    path = path + '/'
    file_name = path + ID

    # Load subtitle data as json
    f = open(file_name + ".sub")
    data = json.load(f)
    f.close()

    # Strip off 0 timestamp if it exists (it usually only exists for auto subs)
    if data['events'][0]['tStartMs'] == 0:
        data['events'].pop(0)

    keys = [d['tStartMs'] for d in data['events']] # Get timestamps
    values = [d['segs'] for d in data['events']]   # Get words

    # Aggregate words into line
    subs = {}
    for key in data['events']:
        sub = ""
        for elem in key['segs']:
            sub = sub + elem['utf8'] + ""

        # Convert ts to seconds
        subs[str(int(key['tStartMs'])/1000)] = sub.replace("\n"," ")

    # Convert to list of only subs
    sub_list = list(subs.values())

    # Write subs to json file
    with open(file_name + '.json', 'w') as f:
        f.write('[\n')
        for i in sub_list:
            f.write("\"" + i + "\",\n")
        f.write('\"EOF\"]')

    # Write subs to csv file using pandas
    (pd.DataFrame.from_dict(data=subs, orient='index')
            .to_csv(file_name + '.csv', header=False))

