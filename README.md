# Jut.su Anime Downloader

This Python script provides an automated way to download anime episodes from the website [jut.su](https://jut.su). It is designed to accept a valid episode URL, the desired video quality, and a directory path for saving the video file. The script then fetches the webpage, parses the HTML content to locate the direct video source URL (usually hosted on Yandex cache servers), and downloads the video file in chunks with a progress bar shown in the console.

## Detailed Description

The script performs the following steps:

1. **Input Validation**  
   - Checks if the input URL matches the expected jut.su anime episode pattern (e.g., `https://jut.su/<anime>/season-<season-number>/episode-<episode-number>.html`).
   - Validates that the selected video quality is one of the supported options: 1080p, 720p, or 480p.

2. **Webpage Parsing**  
   - Sends an HTTP GET request to the episode page with a randomized User-Agent header.
   - Parses the HTML using BeautifulSoup with the `lxml` parser.
   - Finds the `<source>` tag matching the requested quality to extract the direct video URL.
   - Extracts the episode title from the page metadata to use as the filename.

3. **HTTP Session and Headers**  
   - Uses a consistent User-Agent header and sets the `Referer` header to the episode page URL when requesting the video file.
   - Includes the HTTP `Range` header to support chunked downloading and resume capabilities.

4. **Downloading the Video**  
   - Opens a streamed HTTP connection to the video URL.
   - Reads and writes the video content to a file in chunks (default 64 KB).
   - Uses the `tqdm` library to display a real-time progress bar based on the content length.

5. **Logging**  
   - Outputs warnings and info logs at key steps for monitoring the process and troubleshooting.

## Requirements

- Python 3.x  
- `requests` — for HTTP requests  
- `beautifulsoup4` — for HTML parsing  
- `fake-useragent` — to randomize User-Agent headers  
- `tqdm` — for progress bars  
- `lxml` — parser for BeautifulSoup  

You can install dependencies with:

```bash
pip install -r requirements.txt
