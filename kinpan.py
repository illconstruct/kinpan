#/usr/bin/python3
# kinpan.py

import argparse
import os
import sys

from ytdlpsubs import getSubtitles
from ytdlpsubs import getVideoIDs
from ytdlpsubs import convert_ytdlp_subs
from ldaTopics import getTopics

# Supressing output
from contextlib import contextmanager
@contextmanager
def nullify_output(suppress_stdout=True, suppress_stderr=True):
    stdout = sys.stdout
    stderr = sys.stderr
    devnull = open(os.devnull, "w")
    try:
        if suppress_stdout:
            sys.stdout = devnull
        if suppress_stderr:
            sys.stderr = devnull
        yield
    finally:
        if suppress_stdout:
            sys.stdout = stdout
        if suppress_stderr:
            sys.stderr = stderr

# Main
if __name__ == "__main__":

    # Parser
    parser = argparse.ArgumentParser(description="Pull and store subtitles from one or more  YouTube videos.")
    
    # Group
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--channel", action="store_true", help="download subtitles from a given channel")
    group.add_argument("-f", "--file", action="store_true", help="download subtitles from one or more YouTube video links specified in a local file")
    group.add_argument("-y", "--ytlink",action="store_true",help="download subtitles from a given YouTube video link")
    group.add_argument("-p", "--playlist",action="store_true",help="download subtitles from a given YouTube playlist link")
    parser.add_argument("-n", action="store_true", help="if set, do not look for and include topics for subtitles")
    parser.add_argument("input", type=str, help="Enter one of the following: YouTube video URL (-f), YouTube channel URL (-c), YouTube playlist URL (-p), path to a file containing a list of YouTube video URLs (-f)")
        
    # Optional arguments
    parser.add_argument("--lang", type=str, nargs='?', default='en-US', help="Enter a language. Default: \"en-US\"")
    parser.add_argument("--path", type=str, nargs='?', default='subtitles/', help="Enter a directory path for subtitle files to be saved to. Default: \"subtitles/\"")
    
    args = parser.parse_args()

    list_of_videos = []

    # If file
    if args.file:
        file_name = args.input
        with open(file_name) as f:
            vids = f.read().splitlines()

        # Strip to just video IDs
        for idx, i in enumerate(vids):
            if "watch?" in i:
                vids[idx] = i.split("=")[1]

        list_of_videos = vids

    # If link 
    if args.ytlink:
        if "watch?" in args.input:
            list_of_videos.append(args.input.split("v=")[1])
        else:
            list_of_videos.append(args.input)

    # If playlist or channel
    if args.playlist or args.channel:

        with nullify_output(suppress_stdout=True, suppress_stderr=True):
            list_of_videos = getVideoIDs(args.input)

    # Get subtitles
    lang = args.lang

    # Get path
    path = args.path
    if os.path.isdir(path) == False:
        os.mkdir(path)

    # For each video
    for vid_id in list_of_videos:

        # Get subtitles
        with nullify_output(suppress_stdout=True, suppress_stderr=True):
            title, err = getSubtitles(vid_id, lang, path)

        if err == 0:

            # print video info to file
            f = open(path + "/metadata.txt","a")

            # convert json3 subs to json and csv files
            convert_ytdlp_subs(vid_id, path)

            yt_link_base = 'https://www.youtube.com/watch?v='
            print(title + " " + yt_link_base + vid_id)
            f.write(title + "; " + yt_link_base +  vid_id + "; " )

            # return topics
            if args.n == False:
                topics = getTopics(vid_id, path)
                print(topics)
                f.write(str(topics) + "\n")

            f.close()


        else:
            print("Error: Video ID: " + vid_id + " has no subtitles.")
