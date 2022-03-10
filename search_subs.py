#/usr/bin/python3

# search_subs.py
# Helper script: Search through a set of converted YouTube caption .csv files

import time
import re
import sys
import csv
import argparse
import os
import glob

# Main
if __name__ == "__main__":

    # Parser
    parser = argparse.ArgumentParser(description="Search for string across subtitle files.")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--directory", action="store_true", help="search across all .csv files under a given directory")
    group.add_argument("-f", "--file", action="store_true", help="search in the specified .csv file")
   
    parser.add_argument("input", type=str, help="enter either a path to a .csv file using -f (e.g. subtitles/foo.csv) or a path to a directory that contains .csv files using -d (e.g. subtitles/)")
    parser.add_argument("search", type=str, help="the string to search for in subtitle files (e.g. \"house\")")
   
    # Optional
    parser.add_argument("--meta", type=str, nargs='?', default='metadata.txt', help="when using directory, the name of the metadata file in the same directory as the .csv files.  Default is \"metadata.txt\".")
    
    args = parser.parse_args()

    search_str = args.search
    ID = args.input

    # If file
    if args.file:
        match = 0

        with open(ID,'r') as csv_f:

            # Open file
            yt_link_base = 'https://www.youtube.com/watch?v=' + ID.split('/')[-1]
    
            csv_reader = csv.reader(csv_f, delimiter=',')

            for line in csv_reader:
        
                # find match
                matches = re.findall(search_str, line[1])
                if matches:
                    match = 1

                    # convert ts to HMS timestamp
                    ts = time.strftime('%H:%M:%S', time.gmtime(int(float(line[0]))))

                    # add link to YT video for easy access
                    link = yt_link_base + '&t=' + ts.split(':')[0] + 'h' + ts.split(':')[1] + 'm' + ts.split(':')[2] + 's'

                    print(ts + ", " + line[1] + ", " + link)

        if match == 0:
            print("No matches")

    # If directory
    elif args.directory:

        metadata = args.meta

        for filename in glob.glob(ID + '/*.csv'):
            match = 0
            vid_id = filename.split('.')[0].split("/")[1]

            # get and print video title and URL
            with open(ID + "/" + metadata,'r') as f:
                for line in f:

                    if vid_id in line:
                        title = line.split(vid_id)[0] + vid_id
              
                print(title)

            # search through video sbutitles for string
            with open(os.path.join(os.getcwd(), filename), 'r') as csv_f:
                yt_link_base = 'https://www.youtube.com/watch?v=' + vid_id
                csv_reader = csv.reader(csv_f, delimiter=',')

                match = 0

                for line in csv_reader:

                    # find match
                    matches = re.findall(search_str, line[1])
                    if matches:

                        match = 1

                        # convert ts to HMS timestamp
                        ts = time.strftime('%H:%M:%S', time.gmtime(int(float(line[0]))))

                        # add link to YT video for easy access
                        link = yt_link_base + '&t=' + ts.split(':')[0] + 'h' + ts.split(':')[1] + 'm' + ts.split(':')[2] + 's'

                        print(ts + ", " + line[1] + ", " + link)

            if match == 0:
                print ("No matches")

else:
    print("Error.")

