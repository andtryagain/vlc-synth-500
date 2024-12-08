import argparse
import yt_dlp

# Set up argument parsing
parser = argparse.ArgumentParser(description="Download a YouTube video.")

parser.add_argument("url", type=str, help="The URL of the YouTube video to download")

parser.add_argument("--format", type=str, default="mp4", choices=["mp4", "mp3"], help="Import format (mp4 or mp3)")
parser.add_argument("--output", type=str, default="content", help="Download format: 'mp4' (video) or 'mp3' (audio)")

# Parse the arguments
args = parser.parse_args()

# Extract the video URL and output path
video_url = args.url
format = args.format
output_path = args.output

audio_options = {
    'format': 'bestaudio/best',
    'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }
    ],
}

video_options = {
    'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
    'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }],
}

if format == "mp4":
    options = video_options

elif format == "mp3":
    options = audio_options

else:
    raise Exception("Wrong format: mp3 or mp4 is availible!!!")


with yt_dlp.YoutubeDL(options) as ydl:
    ydl.download([video_url])
