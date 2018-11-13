import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description="Command line app to change the video and subtitles into csv file to import in Anki")
parser.add_argument("-v", "--video", help="The video file")
parser.add_argument("-s", "--sub", help="The subtitles file")
parser.add_argument("-o", "--output", help="The name of output file - the one to be imported to Anki")
parser.add_argument("--prefix", help="The prefix to be used when generating the names of pictures and sound")
parser.add_argument("--name", help="The name of video to be added as field - like name of series or movie")
parser.add_argument("--season", help="The season of series - to be added to Anki as field")
parser.add_argument("--episode", help="The episode of the season of series - to be added to Anki as field")
args = parser.parse_args()

if not args.prefix:
    args.prefix = ""
if not args.name:
    args.name == ""
if not args.season:
    args.season = ""
if not args.episode:
    args.episode = ""
if not args.output:
    args.output = "Anki.csv"

def create_video(video, start, end, name):
    subprocess.call(["ffmpeg", "-ss", start, "-to", end, "-i", video, "-b:a", "320K", "-vn", name], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

def create_picture(video, start, name):
    subprocess.call(["ffmpeg", "-ss", start, "-i", video, "-f", "image2", "-vcodec", "mjpeg", "-vframes", "1", name], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

def find_start_and_end_times(times):
    start, end = line.strip().split("-->")
    start = start.strip().split(",")[0]
    end = end.strip().split(",")[0]
    if end[-1] == str(9):
        end = end[:-2] + str(int(end[-2]) + 1) + str(0)
    else:
        end = end[:-1] + str(int(end[-1]) + 1)
    return start, end

def write_line_to_anki(filename, audio, picture, position, line):
    with open(filename, "a") as f:
        f.write(current_line + "\t[sound:" + audio + "]\t<img src='" + picture)
        if args.name:
            f.write("\t" + args.name)
        if args.season:
            f.write("\t" + args.season)
        if args.episode:
            f.write("\t" + args.episode)
        f.write("\n")

with open(args.sub) as f:
    lines = f.readlines()

line_count = 0
for line in lines:
    if line_count == 0:
        position = int(line.strip().replace("\ufeff", ""))
        line_count = line_count + 1
        continue
    if line_count == 1:
        start, end = find_start_and_end_times(line)
        line_count = line_count + 1
        current_line = ""
        continue
    if line_count == 2:
        if not line.strip():
            audio = args.prefix + start.replace(":", "_") + "_" + str(position) + ".mp3"
            picture = args.prefix + start.replace(":", "_") + "_" + str(position)  + ".jpg"
            create_video(args.video, start, end, audio)
            create_picture(args.video, start, picture)
            write_line_to_anki(args.output, audio, picture, position, current_line)
            line_count = 0
            continue
        else:
            current_line = current_line + " " + line.strip()
            current_line = current_line.strip()
