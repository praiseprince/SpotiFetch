import re
import urllib
import yt_dlp
import shutil
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
import subprocess
import os
import threading
import sys
import json
from requests import get, post
from dotenv import load_dotenv
import base64

load_dotenv()
client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
path=os.getenv("DOWNLOAD_PATH")

def get_token():
  auth_string = client_id + ":" + client_secret
  auth_bytes = auth_string.encode("utf-8")
  auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

  url = "https://accounts.spotify.com/api/token"
  headers = {
    "Authorization": "Basic " + auth_base64,
    "Content-Type": "application/x-www-form-urlencoded"
  }
  data = {"grant_type": "client_credentials"}
  result = post(url, headers=headers, data=data)
  json_result = json.loads(result.content)
  token = json_result["access_token"]
  return token

def get_spotify_data(token, url):
  url_types = ("track", "album", "playlist")
  url_type = None
  for type in url_types:
    if type in url:
      url_type = type
      break
  if url_type is None:
    sys.exit("Invalid link.")
  url_format = f"https://open.spotify.com/{url_type}/"
  if not url_format in url:
    sys.exit("The link is Invalid.")
  id = url.replace(url_format, "")
  api_url = f"https://api.spotify.com/v1/{url_type}s/{id}"
  headers = {"Authorization": f"Bearer {token}"}
  result = get(api_url, headers=headers)
  json_result = json.loads(result.content)
  return json_result, url_type

def clean_track(track_data):
  if 'error' in track_data:
    sys.exit("There is an error with the link.")
  track = [{
    'name': track_data['name'],
    'artist': [artist['name'] for artist in track_data['artists']],
    'album': track_data['album']['name'],
    'release_date': track_data['album']['release_date'],
    'track_number': track_data['track_number'],
    'image': track_data['album']['images'][0]['url']
  }]
  return track


def clean_album(album_data):
  if 'error' in album_data:
    sys.exit("There is an error with the link.")
  album_name = album_data['name']
  release_date = album_data['release_date']
  album_images = album_data['images'][0]['url']

  album = [{
    'name': track_data['name'],
    'artist': [artist['name'] for artist in track_data['artists']],
    'album': album_name,
    'release_date': release_date,
    'track_number': track_data['track_number'],
    'image': album_images
  } for track_data in album_data['tracks']['items']]

  return album


def clean_playlist(playlist_data):
  if 'error' in playlist_data:
    sys.exit("There is an error with the link.")

  playlist = [{
    'name':
    track_data['track']['name'],
    'artist': [artist['name'] for artist in track_data['track']['artists']],
    'album':
    track_data['track']['album']['name'],
    'release_date':
    track_data['track']['album']['release_date'],
    'track_number':
    track_data['track']['track_number'],
    'image':
    track_data['track']['album']['images'][0]['url'],
    'playlist':
    playlist_data['name'] + " - " + playlist_data['owner']['display_name']
  } for track_data in playlist_data['tracks']['items']]

  return playlist


def clean_json(json_result, url_type):
  if url_type == "track":
    return clean_track(json_result)
  elif url_type == "album":
    return clean_album(json_result)
  elif url_type == "playlist":
    return clean_playlist(json_result)
  else:
    sys.exit("Invalid link.")

def remove_special_chars(string):
    special_chars = '<>:"/\\|?*'
    new_string = ''.join(c for c in string if c not in special_chars)
    return new_string

def ytdownload(search_query, config):
  search_query=remove_special_chars(search_query)
  encoded_query = urllib.parse.quote(search_query)
  url = f"https://www.youtube.com/results?search_query={encoded_query}"
  html = urllib.request.urlopen(url)
  video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
  vid_url = f"https://www.youtube.com/watch?v={video_id[1]}"
  file_path=f"{config}/{encoded_query}.mp3"
  with yt_dlp.YoutubeDL({
      'extract_audio': True,
      'format': 'bestaudio',
      'outtmpl': file_path
  }) as video:
    info_dict = video.extract_info(vid_url, download=True)
    video_title = info_dict['title']
    print(video_title)
    video.download(vid_url)
    mp3_file_path=f"{config}/{search_query}.mp3"
    subprocess.run(['ffmpeg', '-i', file_path, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', mp3_file_path])
    os.remove(file_path)
    
    return mp3_file_path


def set_metadata(track_data, file_path):
    mp3file = EasyID3(file_path)
    mp3file["albumartist"] = track_data["artist"][0]
    mp3file["artist"] = track_data["artist"]
    mp3file["album"] = track_data["album"]
    mp3file["title"] = track_data["name"]
    mp3file["date"] = track_data["release_date"]
    mp3file["tracknumber"] = str(track_data["track_number"])
    mp3file.save()

    audio = ID3(file_path)
    with urllib.request.urlopen(track_data["image"]) as albumart:
        audio["APIC"] = APIC(
            encoding=3, mime="image/jpeg", type=3, desc="Cover", data=albumart.read()
        )
    audio.save(v2_version=3)

def downloader(data, url_type):
    threads = []
    if url_type == "track":
        track_name = data[0]['name']
        artist_names = ', '.join(data[0]['artist'])
        search_query = f"{track_name} by {artist_names}"
        file_path=ytdownload(search_query, path)
        set_metadata(data[0], file_path)
    elif url_type == "album":
        album=data[0]['album']
        config=f"{path}/{album}"
        for track in data:
            track_name = track['name']
            artist_names = ', '.join(track['artist'])
            search_query = f"{track_name} by {artist_names}"
            t = threading.Thread(target=download_and_set_metadata, args=(search_query, config, track))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        shutil.make_archive(config, 'zip', config)
        shutil.rmtree(config)
    elif url_type=="playlist":
        playlist_name=data[0]['playlist']
        config=f"{path}/{playlist_name}"
        for track in data:
            track_name = track['name']
            artist_names = ', '.join(track['artist'])
            search_query = f"{track_name} by {artist_names}"
            t = threading.Thread(target=download_and_set_metadata, args=(search_query, config, track))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        shutil.make_archive(config, 'zip', config)
        shutil.rmtree(config)

def download_and_set_metadata(search_query, config, track):
    file_path=ytdownload(search_query, config)
    set_metadata(track, file_path)

def main():
   token=get_token()
   url="https://open.spotify.com/playlist/4NTwXnrX6oPYaWV1HA3AZR?si=573217c8dddf4606"
   json_result, url_type=get_spotify_data(token, url)
   clean_data=clean_json(json_result, url_type)
   downloader(clean_data, url_type)

main()