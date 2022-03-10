# Kinpan
Kinpan is a script for scraping captions from a multitude of YouTube videos for rapid digestiblity in terms of indentifying and searching for key topics and phrases. It is intended for use in cybersecurity, specifically Open-Source Intelligence (OSINT) information gathering from YouTube videos, however it has broad applicablilty in terms of honing in on useful or relevant bits of information across an array of videos.

The *kin* in *kinpan* is pronounced *keen* and *pan* is pronounced as in the kitchen appliance, *frying pan*. *Kin* comes from the Japanese word for *gold* and *pan* from the apparatus used to extract gold from sediment, typically from a shallow body of water, a process known as *[Gold panning](https://en.wikipedia.org/wiki/Gold_panning)*.  In this particular case, we are panning for important artifacts (i.e. "gold") from a stream: a YouTube video stream, to be exact.

## Changelog

* 03/01/22: Initial submission

## Dependencies

``python3 (3.6+)``

``python3-pip``

## Python Dependencies

[pandas](https://pandas.pydata.org/), [yt-dlp](https://github.com/yt-dlp/yt-dlp), [gensim](https://radimrehurek.com/gensim/), [nltk](https://www.nltk.org/)

To download:

``pip install pandas yt-dlp gensim nltk``

## Getting Started

Download resources from nltk
``
python3 nltk_dl.py
``

## Tutorial
```
python3 kinpan.py -h [-f | -d | -p | -c] -n INPUT --lang SUBTITLE_LANGUAGE --path PATH
-h		Print help and exit.
-f 		File.  Path to local file containing newline-separated list of YouTube URLs to target.  
-p 		Playlist.  YouTube playlist URL containing videos to target.
-c 		Channel.   YouTube channel URL containing videos to target.
-y 		YouTube link.  Link to YouTube video to target.
-n		No topics. If set, do not return topics for each video. 

Optional inputs
--lang 		Define subtitle language.  If not defined, default is 'en-US'.
--path 		Path to store subtitle files.  If not defined, default is 'subtitles/'.

Example for file download:
python3 kinpan.py -f list.txt --lang en-US --path subtitles

Where list.txt is populated as follows:
https://www.youtube.com/watch?v=ABCDEFG
https://www.youtube.com/watch?v=HIJKLMN
VWXYZAB
https://www.youtube.com/watch?v=OPQRSTU

(Note: either the full YouTube URL or just the video ID is fine)

Example for YouTube video URL:
python3 kinpan.py -y https://www.youtube.com/watch?v=ABCDEFG

Example for playlist download:
python3 kinpan.py -p https://www.youtube.com/playlist?list=ABCDEFG 

Example for channel download:
python3 kinpan -c https://www.youtube.com/c/ABCDEFG

```

```
python3 searchsub.py -h [-f | -d] INPUT --meta FILE
-h		Print help and exit.
-f		File.  CSV file containing subtitles to search through.
                Format of CSV subtitle file is the output of kinpan.py.
-d		Directory.  Path to directory containing CSV subtitle files to search through.
                Format of directory and files is the output of kinpan.py.

Optional inputs:
--meta		Define metadata file located in the directory path.
                File contains the title and video ID of each subtitle file in directory path and is the output of kinpan.py.
                If not defined, default is 'metadata.txt'.

Example for file search for the word 'house':
python3 search_subs.py -f ABCEDFG.csv house

Example for directory search for the word 'house':
python3 search_subs.py -d subtitles/ house --meta metadata.txt

```

## Breakdown

### kinpan.py
1. Use yt-dlp library to identify a list of YouTube video IDs to scrape captions from. The output is stored as ``.json3`` format in a file with the naming convention ``video_ID.sub`` at the location specified by  the``path`` input, which defaults to ``subtitles/``.  The video title and video ID of each video is stored in a file named ``metadata.txt``, also in the location determined by ``path``. Example output:
```
subtitles/ABCDEFG.sub
subtitles/metadata.txt
```

2. Convert the ``.sub`` file into more conventional ``.json`` and ``.csv`` formats and store in the same directory with the naming convention ``video_ID.json`` and ``video_ID.csv``. The ``.json`` file contains only the text of the captions, while the ``.csv`` contains the captions plus their corresponding timestamps. Example output:
```
subtitles/ABCDEFG.json
subtitles/ABCDEFG.csv
```

3. Unless suppressed using ``-n``, a list of 10 topics associated with each video is printed alongside the title and video ID.  These topics are determined using an NTLK/Gensim-supported [LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) algorithm.  A list of [stop words](https://en.wikipedia.org/wiki/Stop_word) for LDA is defined both by [NTLK's default list of stop words](https://pythonspot.com/nltk-stop-words/) and a custom list of stopwords defined in ``stopwords_custom.py``.  This list of stop words may be modified in ``ldaTopics.py`` file to suit one's needs. Example output:
```
This is the Title of a Youtube Video!, https://www.youtube.com/watch?v=ABCDEFG
['topicone, 'topictwo', topicthree', 'topicfour', 'topicfive, 'topicsix', topicseven', 'topiceight', 'topicnine', 'topicten']
```

### search_subs.py
Search for matches for a certain string in either a ``.csv`` file or a directory containing ``.csv`` files generated from the output of Step (2) in the kinpan.py section above.

If searching for a specific file: print out all lines where the string matches with a corresponding timestamp, and YouTube link to that specific timestamp.

If searching across all files in a directory: print out the above, but also associate with each video's title and YouTube link, determined by ``metadata.txt``, which is the output of Step (1) in the kinpan.py section above.

Example output:
```
This is the Title of a Youtube Video!, https://www.youtube.com/watch?v=ABCDEFG
00:01:00, I live in a house, https://www.youtube.com/watch?v=ABCDEFG&t=0h1m0s
00:02:00, You live in a house, https://www.youtube.com/watch?v=ABCDEFG&t=0h2m0s
```
## Roadmap (maybe)
* For videos with no captions, pull audio using yt-dlp, convert with timestamps using STT, and process text to look like yt-dlp sub download format.

## License
Copyright (c) 2022

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---
