# Welcome to SpotiFetch Repository

SpotiFetch is a seamless web app created using `Python`, `Flask`, `HTML`, and `CSS`, enabling users to effortlessly download songs, playlists, or albums from Spotify.

## Screenshots

![Screenshot](https://github.com/praiseprince/SpotiFetch/blob/main/static/styles/Assets/Readme%20Screenshot.png)

## How It Works

1. User provides a Spotify link.
2. The app makes Spotify API calls based on the link and retrieves JSON data.
3. JSON data is cleaned and processed to construct a search string.
4. The search string is used to find content on YouTube.
5. [`yt-dlp`](https://pypi.org/project/yt-dlp/) library downloads content from YouTube.
6. [`ffmpeg`](https://ffmpeg.org/documentation.html) converts the content to MP3 format.
7. Metadata (album art, album name, artists, release date) is added to the MP3 file using the [`mutagen`](https://pypi.org/project/mutagen/) library.
8. If the input is a track, the user receives a single MP3 file. If it's an album or playlist, a zip file is provided.

## Repository Structure

- ```main.py```: This file contains the Flask integration for SpotiFetch. It includes routes that interact with the user, receive the Spotify link, and trigger the downloading and processing of content.

- ```SpotiFetch.py```: This Python script is the heart of the content processing logic. It contains functions for making API calls to Spotify, constructing search queries for YouTube, using yt-dlp to download content, using ffmpeg for conversion, and mutagen for adding metadata. This script orchestrates the entire process of fetching, downloading, and enhancing the content.

- ```requirements.txt```: This file lists all the Python dependencies required to run the application.

- ```.env```: This file is used for storing sensitive environment variables, such as client ID, client secret, and temporary file path.

- ```templates/```: This folder contains the HTML template used for rendering the main page where users input the Spotify link and interact with the app.

- ```static/```: This folder holds static assets such as CSS file, images and icons.

## Getting Started

1. Clone the repository using the following command:
   ```
   git clone https://github.com/praiseprince/SpotiFetch.git
   ```

2. Install the required packages using pip:
   ```
   pip install -r requirements.txt
   ```
3. Install [`ffmpeg`](https://ffmpeg.org/download.html) if you don't have it already.
4. Create a [`Spotify developers account`](https://developer.spotify.com/dashboard/), create an app, and obtain the client ID and client secret.
5. Create a ```.env``` file in the project root directory and add the following information:
   ```
   CLIENT_ID="<your-client-id>"
   CLIENT_SECRET="<your-client-secret>"
   TEMP_PATH="<path-to-store-intermediary-files>"
   ```
6. Run the server to set up the web app locally.
7. Access the web app by visiting the link your IDE provides in your browser.

## Disclaimer
This project is for educational and personal use only. Respect copyright and terms of use when downloading content from Spotify and YouTube.

