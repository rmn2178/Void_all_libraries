import yt_dlp


def download_high_quality_video(url):
    ydl_opts = {
        # 'bestvideo+bestaudio' grabs the highest resolution and highest bitrate audio
        # 'best' is the fallback if separate streams aren't found
        'format': 'bestvideo+bestaudio/best',

        # Merge them into an mp4 or mkv container
        'merge_output_format': 'mp4',

        # Name the file based on the video title
        'outtmpl': '%(title)s.%(ext)s',

        # Optional: helpful for debugging
        'quiet': False,
        'no_warnings': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("\nDownload complete!")
        except Exception as e:
            print(f"An error occurred: {e}")


# Replace with your video URL
video_url = 'https://www.youtube.com/watch?v=your_video_id'
download_high_quality_video(video_url)