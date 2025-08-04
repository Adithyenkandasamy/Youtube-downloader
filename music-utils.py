import os
import re
from yt_dlp import YoutubeDL
from urllib.parse import urlparse, parse_qs

# ✅ Make sure audio output folder exists
output_dir = os.path.join('static', 'audios')
os.makedirs(output_dir, exist_ok=True)

# ✅ Output template for MP3 file
outtmpl = os.path.join(output_dir, '%(title)s.%(ext)s')

# ✅ (Optional) Mask IPs in info files
def mask_ip_addresses(json_str):
    return re.sub(
        r'(ip(?:=|%3D|\/))((?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)|[0-9a-f]{1,4}(?:(?::|%3A)[0-9a-f]{1,4}){7})',
        r'\g<1>0.0.0.0',
        json_str,
        flags=re.IGNORECASE
    )

# ✅ Safe title for filenames
def get_safe_title(title):
    return ''.join(c if c.isalnum() else '_' for c in title)

# ✅ Extract YouTube video ID from URL
def extract_video_id(url):
    query = urlparse(url).query
    return parse_qs(query).get("v", [None])[0]

# ✅ Download YouTube audio with bypasses
def youtube_down(link):
    print("🔍 Extracting video ID...")
    video_id = extract_video_id(link)

    if not video_id:
        print("❌ Invalid YouTube URL!")
        return

    # ✅ yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'writesubtitles': False,        # 🔒 Disable subtitle fetching to avoid HTTP 429
        'writeautomaticsub': False,     # 🔒 Disable auto subtitles too
        'writethumbnail': True,
        'writeinfojson': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        print("⬇️  Downloading audio...")
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_id, download=False)

            video_info = {
                'id': info.get('id'),
                'title': info.get('title'),
                'author': info.get('uploader'),
                'views': info.get('view_count'),
                'length': info.get('duration'),
                'description': info.get('description'),
            }

            ydl.download([video_id])
            print(f"✅ Downloaded: {video_info['title']}")
            return video_info['id'], get_safe_title(video_info['title'])

    except Exception as e:
        print("❌ Error:", str(e))

# ✅ CLI Entry
if __name__ == '__main__':
    link = input("🔗 Enter YouTube video URL: ").strip()
    youtube_down(link)
