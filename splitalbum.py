
import sys
import re
import sys
import subprocess

def divide_mp3(infile, time_start, time_end, outfile):
    subprocess.Popen(["ffmpeg","-i",infile,"-vn","-acodec","copy","-ss",f"00:{time_start}","-to", f"00:{time_end}", outfile]).communicate()

def set_metadata(path, artist, album, title, year):
    proc = subprocess.Popen(["id3v2","-a",artist,"-A",album, "-t", title, "-y", str(year), path], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(proc.communicate())

#line_pattern = re.compile(r"^[0-9]{1,3} ?- ?(?P<title>[^\(]+) \((?P<from>[0-9:]+) ?- ?(?P<to>[0-9:]+)\)")
line_pattern = re.compile(r"^[0-9]{1,3} (?P<artist>[^-]+) - (?P<title>[^\[]+) \[(?P<from>[0-9:]+)-(?P<to>[0-9:]+)\]")

album = "Mix 4 A M D I S C S"
year = 2016
#artist = "VANGUARD"
if __name__ == "__main__":
    _,albumfile,timestamps = sys.argv
    with open(timestamps) as f:
        timestamps = f.readlines()
    for line in timestamps:
        if not line:
            continue
        m = line_pattern.match(line)
        if m:
            data = m.groupdict()
            outfile = f"{data['artist']} - {data['title']}.mp3"
            divide_mp3(albumfile,data["from"],data["to"],outfile)
            set_metadata(outfile, data['artist'], album, data["title"], year)
        else:
            print(line)


