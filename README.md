# Subtitles2Anki Script

This is a script for creating quick ANKI cards for studying for the video and subtitles. 

## Installation

### Installing Python

In order to use this script, you would need to have Python3 installed on your system. If you are using Mac and Linux, Python is already installed on your system. Not sure about the Windows, since I am not using it. 

You can check if Python is installed by running the following commands in your command prompt.

```
python --version
python3 --version
```

If you see something like `Python 3.11.4` (the first 3 is important, the latter numbers could be anything), then you have Python installed. If not, follow the guides on the official Python site: https://wiki.python.org/moin/BeginnersGuide/Download

### Installing ffmpeg

Install ffmpeg with the package manage of your choice. This is most likely going to be brew on Mac and a variation of apt-get / pacman / ...

### Installing the Program

This program is just a one file script and therefore does not require the installation. You just need to download it to your computer.

## Running the program

To run a program, run it with Python, name of the files and the required arguments. So the command would look something like this:

```
python subtitles2anki.py -s subtitles.srt -v video.mp4
```

The results would be the CSV file that can be imported into ANKI and the pictures and audio files that accompany it.

### Arguments

The program supports additional parameters. They are listed below. They could also be accessed with the --help flag.

```
-v VIDEO, --video VIDEO     The video file
-s SUB, --sub SUB           The subtitles file
-o OUTPUT, --output OUTPUT. The name of output file - the one to be imported to Anki
--prefix PREFIX       The prefix to be used when generating the names of pictures and sound
--name NAME           The name of video to be added as field - like name of series or movie
--season SEASON       The season of series - to be added to Anki as field
--episode EPISODE     The episode of the season of series - to be added to
--padding PADDING     How much padding to add on the begging and the end of the audio in miliseconds
--folder FOLDER       In which folder are the files saved - requires absolute filepath or relative to running script
```