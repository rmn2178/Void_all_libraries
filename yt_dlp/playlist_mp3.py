import yt_dlp


def download_playlist_as_mp3(playlist_url):
    ydl_opts = {
        # Select best audio quality
        'format': 'bestaudio/best',

        # Download all videos in the playlist
        'yes_playlist': True,

        # Post-processor to extract audio and convert to mp3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],

        # Save files in a subfolder named after the playlist
        # Format: Playlist Name / Song Title.mp3
        'outtmpl': '%(playlist_title)s/%(title)s.%(ext)s',

        # Ignore errors to keep downloading if one video in the list is blocked/deleted
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


# Replace with your YouTube Playlist URL
playlist_url = 'https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID'
download_playlist_as_mp3(playlist_url)