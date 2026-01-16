import yt_dlp


def download_youtube_mp3(url):
    ydl_opts = {
        # Select the best quality audio
        'format': 'bestaudio/best',

        # Post-processor to convert the file to mp3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Highest MP3 bitrate
        }],

        # Name the file based on the song title
        'outtmpl': '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("\nMP3 download complete!")
        except Exception as e:
            print(f"An error occurred: {e}")


# Replace with your song URL
song_url = 'https://www.youtube.com/watch?v=example'
download_youtube_mp3(song_url)