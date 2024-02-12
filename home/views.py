from django.shortcuts import render
from django.http import HttpResponse
from django.http import request
from pytube import YouTube
import re
import os


def download_audio_and_video(url, format_choice):
    try:
        yt = YouTube(url)
        title = re.sub(r'[^\w\s]', '', yt.title) 

        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        if format_choice.lower() == "mp3":
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=downloads_path, filename=f"{title}.mp3")
            print("MP3 download completed successfully!")
            return HttpResponse("<script>alert('MP3 download completed successfully!'); window.location.href = '/';</script>")


        elif format_choice.lower() == "mp4":
            video_stream = yt.streams.filter(file_extension='mp4').first()
            video_stream.download(output_path=downloads_path, filename=f"{title}.mp4")
            print("MP4 download completed successfully!")
            return HttpResponse("<script>alert('MP4 download completed successfully!'); window.location.href = '/';</script>")
        elif format_choice.lower() == "both":
            audio_stream = yt.streams.filter(only_audio=True).first()
            video_stream = yt.streams.filter(file_extension='mp4').first()
            audio_stream.download(output_path=downloads_path, filename=f"{title}.mp3")
            video_stream.download(output_path=downloads_path, filename=f"{title}.mp4")
            print("MP3 and MP4 download completed successfully!")
            return HttpResponse("<script>alert('MP3 and MP4 download completed successfully!'); window.location.href = '/';</script>")
        else:
            raise ValueError("Invalid choice! Please choose 'mp3', 'mp4', or 'both'.")
    except Exception as e:
        return render(None, 'error.html', {'error_message': str(e)})

def youtube_downloader(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        format_choice = request.POST.get('format')
        
        result = download_audio_and_video(url, format_choice)
        if isinstance(result, HttpResponse):
            return result 
    return render(request, 'index.html')  
