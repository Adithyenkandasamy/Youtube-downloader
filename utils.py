import os
import re
from yt_dlp import YoutubeDL

# Function to mask IP addresses in JSON string
def mask_ip_addresses(json_str):
    return re.sub(
        r'(ip(?:=|%3D|\/))((?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)|[0-9a-f]{1,4}(?:(?::|%3A)[0-9a-f]{1,4}){7})',
        r'\g<1>0.0.0.0',
        json_str,
        flags=re.IGNORECASE
    )

# Ensure the 'videos' directory exists
output_dir = 'videos'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# in the title if there is any special character it will be replaced by _ and the file will be saved

outtmpl=os.path.join('static', output_dir,'%(title)s.%(ext)s')
def youtube_down(link):
    print("inside youtube_down")

    video_id = link.split('v=')[-1].split('&')[0]
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        # instead of title we can use %(id)s to save the file with the video id
        'outtmpl': os.path.join('static', output_dir,'%(title)s.%(ext)s'),
        'writesubtitles': True,
        'writeautomaticsub': True,
        'writethumbnail': True,
        'writeinfojson': True,
        'noplaylist': True,
        'quiet': True,
    }

    try:
        print("inside try")
        with YoutubeDL(ydl_opts) as ydl:
            # Fetch video info
            info_dict = ydl.extract_info(video_id, download=False)
            
            
            # # Extract relevant info
            video_info = {
                'id': info_dict.get('id', None),
                'title': info_dict.get('title', None),
                'rating': info_dict.get('average_rating', None),
                'author': info_dict.get('uploader', None),
                'views': info_dict.get('view_count', None),
                'length': info_dict.get('duration', None),
                'description': info_dict.get('description', None),
            }
            
            
            # Download the highest quality video
            ydl.download([video_id])
            
            print('Video downloaded successfully', video_info['title'])
            return video_info['id'],get_safe_title(video_info['title'])

    except Exception as e:
        print('Error:', str(e))

# Example usage
# youtube_down('https://www.youtube.com/watch?v=YOUR_VIDEO_ID')
import string

def get_safe_title(title):
    x=""
    for i in title:
        if not i.isalnum():
            x+="_"
        else:
            x+=i
    return x


if __name__ == '__main__':
    youtube_down(input('Enter YouTube video URL: '))