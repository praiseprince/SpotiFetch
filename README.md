# SpotiFetch

SpotiFetch is a web app that allows you to download playlists, albums, or tracks from Spotify. It leverages the Spotify API to fetch JSON data from given links, processes and cleans the data, searches for corresponding content on YouTube, downloads using the yt-dlp library, converts to MP3 format using ffmpeg, adds metadata including album art, album name, artists, and release date, and finally delivers the content to the user.

## Screenshots

![Screenshot](screenshot.png)

## How It Works

1. User provides a Spotify link.
2. The app makes Spotify API calls based on the link and retrieves JSON data.
3. JSON data is cleaned and processed to construct a search string.
4. The search string is used to find content on YouTube.
5. 'yt-dlp' library downloads content from YouTube.
6. ffmpeg converts the content to MP3 format.
7. Metadata (album art, album name, artists, release date) is added to the MP3 file.
8. If the input is a track, the user receives a single MP3 file. If it's an album or playlist, a zip file is provided.

## Technologies Used

- HTML
- CSS
- Python
- Flask

## Getting Started

1. Clone the repository using the following command:
   ```
   git clone https://github.com/praiseprince/SpotiFetch.git
   ```

2. Install the required packages using pip:
   ```
   pip install -r requirements.txt
   ```
3. Install ffmpeg if you don't have it already.
4. Create a [Spotify developers account](https://developer.spotify.com/dashboard/), create an app, and obtain the client ID and client secret.
5. Create a '.env' file in the project root directory and add the following information:
   ```
   CLIENT_ID='<your-client-id>'
   CLIENT_SECRET='<your-client-secret>'
   TEMP_PATH='<path-to-store-intermediary-files>'
   ```
6. Run the server to set up the web app locally.
7. Access the web app by visiting the link your IDE provides in your browser.

## Disclaimer
This project is for educational and personal use only. Respect copyright and terms of use when downloading content from Spotify and YouTube.

Remember to replace '<your-client-id>', '<your-client-secret>', and '<path-to-store-intermediary-files>' with appropriate values in the `.env` file.

