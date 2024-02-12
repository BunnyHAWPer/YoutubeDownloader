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

        # Get user's Downloads folder path
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        if format_choice.lower() == "mp3":
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=downloads_path, filename=f"{title}.mp3")
            print("MP3 download completed successfully!")
            return HttpResponse("""
    <style>
    .modal {
        display: none;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0, 0, 0, 0.4);
    }

    .modal-content {
        background-color: #fefefe;
        margin: 15% auto;
        padding: 20px;
        border: 1px solid #888;
        width: 80%;
    }
    </style>

    <div id="myModal" class="modal">
        <div class="modal-content">
            <p>Download completed successfully!</p>
        </div>
    </div>

    <script>
    var modal = document.getElementById('myModal');
    modal.style.display = 'block';
    setTimeout(function() {
        modal.style.display = 'none';
        window.location.href = '/';
    }, 3000); // Adjust the timeout as needed (3000ms = 3 seconds)
    </script>
""")


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
        # Render error page with error message
        return render(None, 'error.html', {'error_message': str(e)})

def youtube_downloader(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        format_choice = request.POST.get('format')
        
        result = download_audio_and_video(url, format_choice)
        if isinstance(result, HttpResponse):
            return result  # If download succeeded, return success response
    return render(request, 'index.html')  # Render index page if method is GET or if an error occurred


# Working 

# def download_audio_and_video(url, format_choice):
#     try:
#         yt = YouTube(url)
#         title = re.sub(r'[^\w\s]', '', yt.title) 

#         # Get user's Downloads folder path
#         downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

#         if format_choice.lower() == "mp3":
#             audio_stream = yt.streams.filter(only_audio=True).first()
#             audio_stream.download(output_path=downloads_path, filename=f"{title}.mp3")
#             print("MP3 download completed successfully!")
#         elif format_choice.lower() == "mp4":
#             video_stream = yt.streams.filter(file_extension='mp4').first()
#             video_stream.download(output_path=downloads_path, filename=f"{title}.mp4")
#             print("MP4 download completed successfully!")
#         elif format_choice.lower() == "both":
#             audio_stream = yt.streams.filter(only_audio=True).first()
#             video_stream = yt.streams.filter(file_extension='mp4').first()
#             audio_stream.download(output_path=downloads_path, filename=f"{title}.mp3")
#             video_stream.download(output_path=downloads_path, filename=f"{title}.mp4")
#             print("MP3 and MP4 download completed successfully!")
#         else:
#             print("Invalid choice! Please choose 'mp3', 'mp4', or 'both'.")
#     except Exception as e:
#         print("An error occurred:", str(e))



# def download_audio_and_video(url, format_choice):
#     try:
#         yt = YouTube(url)
#         title = re.sub(r'[^\w\s]', '', yt.title) 

#         if format_choice.lower() == "mp3":
#             audio_stream = yt.streams.filter(only_audio=True).first()
#             audio_stream.download(filename=f"{title}.mp3")
#             print("MP3 download completed successfully!")
#         elif format_choice.lower() == "mp4":
#             video_stream = yt.streams.filter(file_extension='mp4').first()
#             video_stream.download(filename=f"{title}.mp4")
#             print("MP4 download completed successfully!")
#         elif format_choice.lower() == "both":
#             audio_stream = yt.streams.filter(only_audio=True).first()
#             video_stream = yt.streams.filter(file_extension='mp4').first()
#             audio_stream.download(filename=f"{title}.mp3")
#             video_stream.download(filename=f"{title}.mp4")
#             print("MP3 and MP4 download completed successfully!")
#         else:
#             print("Invalid choice! Please choose 'mp3', 'mp4', or 'both'.")
#     except Exception as e:
#         print("An error occurred:", str(e))

# working 
# def youtube_downloader(request):
#     if request.method == 'POST':
#         url = request.POST.get('url')
#         format_choice = request.POST.get('format')
        
#         download_audio_and_video(url, format_choice)
#         return HttpResponse("Download completed successfully!")
#     else:
#         return render(request, 'index.html')
