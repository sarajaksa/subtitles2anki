import subprocess
import os

filename = "Flash-Season1-Episode1-34:20-37:07-FlashesFirstFight.srt"
add_to_name = "Flash-Season1-Episode1-"
video = "Flash-Season1-Episode1.mkv"
filename_output = "Anki.csv"
series = "Flash"
season = "2"
episode = "1"

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
        f.write(current_line)
        f.write("\t")
        f.write("[sound:")
        f.write(audio)
        f.write("]")
        f.write("\t")
        f.write("<img src='")
        f.write(picture)
        f.write("'>")
        f.write("\t")
        f.write(series)
        f.write("\t")
        f.write(season)
        f.write("\t")
        f.write(episode)
        f.write("\n")

with open(filename) as f:
    lines = f.readlines()

line_count = 0

with open("Anki.csv", "w") as f:
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
                audio = add_to_name + start.replace(":", "_") + ".mp3"
                picture = add_to_name + start.replace(":", "_")  + ".jpg"
                create_video(video, start, end, audio)
                create_picture(video, start, picture)
                write_line_to_anki(filename_output, audio, picture, position, current_line)
                line_count = 0
                print(position)
                continue
            else:
                current_line = current_line + " " + line.strip()
                current_line = current_line.strip()



