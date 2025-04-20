
# Chroma Video Downloader

A beautiful, feature-rich video downloading application with a modern UI and animations. Powered by yt-dlp and aria2c.

![Chroma Video Downloader](https://i.imgur.com/DwbjuKR.png)

## Features

- 🎨 **Beautiful Modern UI** with animations, transitions, and a responsive design
- 🚀 **Fast Downloads** using aria2c for multi-connection acceleration
- 🎬 **Video Quality Selection** with resolution, format, and size information
- 🎵 **Audio Extraction** option to download just the audio as MP3
- 📊 **Download Progress** visualization
- 📂 **Download Management** to see and access your downloaded files
- 🎛️ **Customization Options** including custom filenames

## Requirements

- Python 3.7 or higher
- aria2c (optional, but recommended for faster downloads)

## Quick Start

1. Clone this repository or download the files
2. Make sure Python 3.7+ is installed
3. Run the start script:

```bash
python start.py
```

This will:
- Check for and install required dependencies
- Create the downloads directory
- Start the web server on port 8000
- Open your browser to http://localhost:8000

Alternatively, you can run the app directly:

```bash
python app.py
```

## Manual Installation

If you prefer to install dependencies manually:

```bash
pip install flask yt-dlp
```

To install aria2c (optional but recommended for faster downloads):

- **Linux**: `sudo apt install aria2`
- **macOS**: `brew install aria2`
- **Windows**: `choco install aria2` or download from the [official releases](https://github.com/aria2/aria2/releases)

## Usage

1. Paste a video URL in the input field
2. Click "Get Video Info" to fetch available formats
3. Select your preferred quality/format
4. Customize options (filename, audio-only, etc.)
5. Click "Download" to start downloading
6. Access your downloaded files from the Downloads section

## Customization

You can customize the app by modifying the following:

- **UI Colors**: Edit the CSS variables in the `index.html` file
- **Download Folder**: Change the `DOWNLOAD_FOLDER` in `app.py`
- **Port**: Change the port in `app.py` if 8000 is already in use

## License

This project is open source and available under the MIT License.

## Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The core video extraction library
- [aria2](https://aria2.github.io/) - For accelerated downloads
- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Font Awesome](https://fontawesome.com/) - For the beautiful icons
