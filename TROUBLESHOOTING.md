
# Troubleshooting Guide

This guide covers common issues you might encounter when using Chroma Video Downloader and how to resolve them.

## Common Issues

### Application won't start

**Issue**: When running `python app.py`, you get an error about missing modules.

**Solution**: Make sure you've installed all required dependencies:

```bash
pip install flask yt-dlp
```

Or run the `start.py` script which will automatically install dependencies:

```bash
python start.py
```

### Downloads fail with aria2c errors

**Issue**: Downloads fail with errors related to aria2c.

**Solution**: 

1. Make sure aria2c is installed on your system:
   - Linux: `sudo apt install aria2`
   - macOS: `brew install aria2`
   - Windows: `choco install aria2` or download from official site

2. If you still have issues, uncheck the "Use aria2c for faster downloads" option in the UI.

### Video information can't be retrieved

**Issue**: When entering a URL, you get an error about failing to extract video information.

**Solutions**:

1. Verify the URL is correct and the video exists
2. Some platforms may restrict access - try a different video
3. Update yt-dlp to the latest version: `pip install -U yt-dlp`
4. Check if the site is supported by yt-dlp

### Downloads folder not found

**Issue**: You get errors about the downloads folder not existing.

**Solution**: Create the `downloads` folder in the same directory as the app.py file:

```bash
mkdir downloads
```

### Port 8000 is already in use

**Issue**: You get an error that port 8000 is already in use.

**Solution**: Change the port in app.py by modifying this line:

```python
app.run(host='0.0.0.0', port=8000, debug=False)
```

Change 8000 to any other port number (e.g., 8080, 9000).

### Application is slow to show video information

**Issue**: The app takes a long time to show video information.

**Solution**: This is normal for some videos, especially from sites with rate limiting. The application is working to retrieve the available formats. For very popular videos on certain platforms, this process can take a bit longer.

## Advanced Configuration

### Using a custom download folder

If you want to change the downloads folder location, modify the following line in `app.py`:

```python
app.config['DOWNLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
```

Change it to your preferred path.

### Adding custom format options

To add additional format options, you would need to modify the `/api/video-info` endpoint in `app.py` to include the additional formats you want to support.

## Getting Help

If you encounter an issue not covered in this guide, please:

1. Check the console output for error messages
2. Make sure all dependencies are up to date
3. Try using the app without aria2c by unchecking the option in the UI
4. Check if yt-dlp supports the site you're trying to download from
