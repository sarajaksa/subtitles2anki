from functools import partial
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
parser.add_argument("--padding", help="How much padding to add on the begging and the end of the audio in miliseconds")
args = parser.parse_args()

class AnkizationSubtitles():

    def __init__(self, args):
        self.args = args
        if not self.args.prefix:
           self. args.prefix = ""
        if not args.name:
            self.args.name == ""
        if not args.season:
            self.args.season = ""
        if not args.episode:
            self.args.episode = ""
        if not args.output:
            self.args.output = "Anki.csv"
        if not args.padding:
            self.args.padding = 0
        self.args.padding = int(self.args.padding)

        self.add_padding_start = partial(self.add_padding_to_times, direction=-1)
        self.add_padding_end = partial(self.add_padding_to_times, direction=1)

        self.lines = self.open_subtitles(self.args.sub)
        self.format_subtitles_to_flashcards(self.lines, self.args.prefix, self.args.output, self.args.padding)

    def create_video(self, video, start, end, name):
        subprocess.call(["ffmpeg", "-ss", start, "-to", end, "-i", video, "-b:a", "320K", "-vn", name], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

    def create_picture(self, video, start, name):
        subprocess.call(["ffmpeg", "-ss", start, "-i", video, "-f", "image2", "-vcodec", "mjpeg", "-vframes", "1", name], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

    def find_start_and_end_times(self, times, padding):
        start, end = times.strip().split("-->")
        start = start.strip().replace(",", ".")
        end = end.strip().replace(",", ".")
        start = self.add_padding_start(start, padding)
        end = self.add_padding_end(end, padding)
        return start, end

    def add_padding_to_times(self, time, padding, direction):
        time_units_max = {0: 1000, 1:60, 2:60, 3:24}
        time_units = time.split(":")
        time_units = time_units[:-1] + time_units[-1].split(".")
        time_units = [int(i) for i in time_units][::-1]
        for i, _ in enumerate(time_units):
            time_units[i] = time_units[i] + padding * direction
            if time_units[i] >= time_units_max[i] or time_units[i] < 0:
                padding = 0
                while time_units[i] >= time_units_max[i] or time_units[i] < 0:
                    padding = padding + 1
                    time_units[i] = time_units[i] - time_units_max[i] * direction
            else:
                break
        hours, minutes, seconds, miliseconds = time_units[::-1]
        return "{}:{}:{}.{}".format(hours, minutes, seconds, miliseconds)

    def write_line_to_anki(self, filename, audio, picture, position, line):
        with open(filename, "a") as f:
            f.write(line + "\t[sound:" + audio + "]\t<img src='" + picture + "'>")
            if args.name:
                f.write("\t" + args.name)
            if args.season:
                f.write("\t" + args.season)
            if args.episode:
                f.write("\t" + args.episode)
            f.write("\n")

    def open_subtitles(self, subtitles):
        with open(subtitles) as f:
            lines = f.readlines()
        return lines

    def get_line_position(self, line):
        return int(line.strip().replace("\ufeff", ""))

    def create_current_line(self, line_so_far, line):
        current_line = line_so_far + " " + line.strip()
        return current_line.strip()

    def create_anki_flashcard(self, prefix, start, end, position, line, output_file):
        audio = prefix + start.replace(":", "_") + "_" + str(position) + ".mp3"
        picture = prefix + start.replace(":", "_") + "_" + str(position)  + ".jpg"
        self.create_video(args.video, start, end, audio)
        self.create_picture(args.video, start, picture)
        self.write_line_to_anki(output_file, audio, picture, position, line)

    def format_subtitles_to_flashcards(self, lines, prefix, output, padding):
        line_count = 0
        for line in lines:
            if line_count == 0:
                position = self.get_line_position(line)
                line_count = line_count + 1
                continue
            if line_count == 1:
                start, end = self.find_start_and_end_times(line, padding)
                line_count = line_count + 1
                current_line = ""
                continue
            if line_count == 2:
                if not line.strip():
                    self.create_anki_flashcard(prefix, start, end, position, current_line, output)
                    print(position)
                    line_count = 0
                    continue
                else:
                    current_line = self.create_current_line(current_line, line)

if __name__ == "__main__":
    AnkizationSubtitles(args)
