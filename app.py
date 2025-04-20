
#!/usr/bin/env python3
import os
import json
import subprocess
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, Response, stream_with_context
import yt_dlp

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/video-info', methods=['POST'])
def get_video_info():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Format the data to return to frontend
            formats = []
            for f in info.get('formats', []):
                if f.get('resolution') != 'audio only' and f.get('fps') is not None:
                    format_info = {
                        'format_id': f.get('format_id'),
                        'extension': f.get('ext'),
                        'resolution': f.get('resolution'),
                        'fps': f.get('fps'),
                        'filesize': f.get('filesize'),
                        'vcodec': f.get('vcodec')
                    }
                    formats.append(format_info)
            
            # Sort formats by quality (approximate)
            formats.sort(key=lambda x: (
                0 if x['resolution'] is None else int(x['resolution'].split('x')[1]) if 'x' in x['resolution'] else int(x['resolution'][:-1]) if x['resolution'].endswith('p') else 0,
                x['fps'] or 0
            ), reverse=True)
            
            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'formats': formats
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    format_id = data.get('format_id')
    audio_only = data.get('audio_only', False)
    filename = data.get('filename', '')
    use_aria = data.get('use_aria', True)
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        download_opts = {
            'quiet': False,
            'progress': True,
            'outtmpl': os.path.join(app.config['DOWNLOAD_FOLDER'], '%(title)s.%(ext)s'),
            'no_warnings': False,
        }
        
        if format_id and not audio_only:
            download_opts['format'] = format_id
        elif audio_only:
            download_opts['format'] = 'bestaudio'
            download_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        
        if filename:
            safe_filename = ''.join(c for c in filename if c.isalnum() or c in ' ._-')
            download_opts['outtmpl'] = os.path.join(app.config['DOWNLOAD_FOLDER'], f'{safe_filename}.%(ext)s')
        
        if use_aria:
            download_opts['external_downloader'] = 'aria2c'
            download_opts['external_downloader_args'] = ['--min-split-size=1M', '--max-connection-per-server=16', '--max-concurrent-downloads=16', '--split=16']
        
        with yt_dlp.YoutubeDL(download_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            # Handle potential postprocessing name changes
            if audio_only and not file_path.endswith('.mp3'):
                file_path = os.path.splitext(file_path)[0] + '.mp3'
            
            if os.path.exists(file_path):
                return jsonify({
                    'success': True, 
                    'message': 'Download completed',
                    'filename': os.path.basename(file_path),
                    'download_url': f'/download/{os.path.basename(file_path)}'
                })
            else:
                # Try to find the file with a different extension
                base_path = os.path.splitext(file_path)[0]
                for ext in ['.mp4', '.webm', '.mkv', '.mp3', '.m4a']:
                    test_path = base_path + ext
                    if os.path.exists(test_path):
                        return jsonify({
                            'success': True,
                            'message': 'Download completed',
                            'filename': os.path.basename(test_path),
                            'download_url': f'/download/{os.path.basename(test_path)}'
                        })
                        
                return jsonify({'error': 'Download completed but file not found'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)

@app.route('/api/downloads')
def list_downloads():
    files = []
    for file in os.listdir(app.config['DOWNLOAD_FOLDER']):
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            files.append({
                'name': file,
                'size': size,
                'size_formatted': format_size(size),
                'download_url': f'/download/{file}'
            })
    return jsonify(files)

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

if __name__ == '__main__':
    print("==============================================")
    print("🚀 Video Downloader Server is running!")
    print("Visit http://localhost:8000 in your browser")
    print("==============================================")
    app.run(host='0.0.0.0', port=8000, debug=False)
