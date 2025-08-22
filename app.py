#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Video Info API
YouTube video ID'si alıp video bilgilerini döndüren API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from pathlib import Path
import yt_dlp
import ssl
import urllib3

# SSL sertifika doğrulamasını tamamen devre dışı bırak
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Python SSL ayarlarını devre dışı bırak
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''

app = Flask(__name__)
CORS(app)

class YouTubeInfoExtractor:
    def __init__(self):
        """
        YouTube bilgi çıkarıcı sınıfını başlat
        """
        pass
        
    def get_video_info(self, url):
        """
        Video bilgilerini al
        
        Args:
            url (str): YouTube video URL'si
            
        Returns:
            dict: Video bilgileri
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            return None
    
    def get_formats(self, url):
        """
        Video formatlarını al
        
        Args:
            url (str): YouTube video URL'si
            
        Returns:
            dict: Video formatları ve bilgileri
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            return None

# Global extractor instance
extractor = YouTubeInfoExtractor()

@app.route('/video/<video_id>', methods=['GET'])
def get_video_info(video_id):
    """
    Video bilgilerini al
    
    Args:
        video_id (str): YouTube video ID'si
    
    Returns:
    {
        "success": true,
        "video_id": "dQw4w9WgXcQ",
        "title": "Video Başlığı",
        "description": "Video açıklaması",
        "duration": 180,
        "duration_formatted": "3:00",
        "uploader": "Kanal Adı",
        "upload_date": "20231201",
        "view_count": 1234567,
        "like_count": 12345,
        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
        "formats": [
            {
                "format_id": "401",
                "ext": "mp4",
                "resolution": "3840x2160",
                "height": 2160,
                "width": 3840,
                "filesize": 123456789,
                "filesize_mb": 117.7,
                "url": "https://...",
                "format_note": "4K"
            }
        ],
        "best_formats": {
            "video": {
                "format_id": "401",
                "ext": "mp4",
                "resolution": "3840x2160",
                "height": 2160,
                "width": 3840,
                "filesize": 123456789,
                "filesize_mb": 117.7,
                "url": "https://...",
                "format_note": "4K"
            },
            "audio": {
                "format_id": "251",
                "ext": "webm",
                "acodec": "opus",
                "abr": 160,
                "filesize": 1234567,
                "filesize_mb": 1.2,
                "url": "https://...",
                "format_note": "Opus 160k"
            }
        }
    }
    """
    try:
        # Video ID'sinin geçerli olup olmadığını kontrol et
        if len(video_id) != 11:
            return jsonify({
                'success': False,
                'message': 'Geçersiz video ID'
            }), 400
        
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Video bilgilerini al
        info = extractor.get_formats(url)
        if not info:
            return jsonify({
                'success': False,
                'message': 'Video bulunamadı veya erişilemiyor'
            }), 404
        
        # Formatları işle
        formats = []
        best_video = None
        best_audio = None
        
        for format_info in info.get('formats', []):
            format_data = {
                'format_id': format_info.get('format_id'),
                'ext': format_info.get('ext'),
                'resolution': format_info.get('resolution', 'N/A'),
                'height': format_info.get('height'),
                'width': format_info.get('width'),
                'filesize': format_info.get('filesize'),
                'filesize_mb': round(format_info.get('filesize', 0) / 1024 / 1024, 1) if format_info.get('filesize') else None,
                'url': format_info.get('url'),
                'format_note': format_info.get('format_note', ''),
                'acodec': format_info.get('acodec'),
                'vcodec': format_info.get('vcodec'),
                'abr': format_info.get('abr'),  # Audio bitrate
                'vbr': format_info.get('vbr'),  # Video bitrate
                'fps': format_info.get('fps'),
                'tbr': format_info.get('tbr'),  # Total bitrate
            }
            
            formats.append(format_data)
            
            # En iyi video formatını bul (sadece video, ses yok)
            if (format_info.get('vcodec') != 'none' and 
                format_info.get('acodec') == 'none' and 
                format_info.get('height')):
                current_height = format_info.get('height')
                if current_height is not None:
                    best_height = best_video.get('height') if best_video else None
                    if not best_video or (best_height is None) or (current_height > best_height):
                        best_video = format_data
            
            # En iyi ses formatını bul (sadece ses)
            if (format_info.get('acodec') != 'none' and 
                format_info.get('vcodec') == 'none'):
                current_abr = format_info.get('abr')
                if current_abr is not None:
                    best_abr = best_audio.get('abr') if best_audio else None
                    if not best_audio or (best_abr is None) or (current_abr > best_abr):
                        best_audio = format_data
        
        # Süreyi formatla
        duration = info.get('duration', 0)
        duration_formatted = f"{duration // 60}:{duration % 60:02d}" if duration else "0:00"
        
        # Yanıt verisi
        response_data = {
            'success': True,
            'video_id': video_id,
            'title': info.get('title', 'Bilinmiyor'),
            'description': info.get('description', ''),
            'duration': duration,
            'duration_formatted': duration_formatted,
            'uploader': info.get('uploader', 'Bilinmiyor'),
            'upload_date': info.get('upload_date', ''),
            'view_count': info.get('view_count', 0),
            'like_count': info.get('like_count', 0),
            'thumbnail': info.get('thumbnail', ''),
            'formats': formats,
            'best_formats': {
                'video': best_video,
                'audio': best_audio
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {e}'
        }), 500

@app.route('/video/<video_id>/formats', methods=['GET'])
def get_video_formats(video_id):
    """
    Sadece video formatlarını al
    
    Args:
        video_id (str): YouTube video ID'si
    
    Returns:
    {
        "success": true,
        "video_id": "dQw4w9WgXcQ",
        "formats": [...],
        "best_formats": {...}
    }
    """
    try:
        # Video ID'sinin geçerli olup olmadığını kontrol et
        if len(video_id) != 11:
            return jsonify({
                'success': False,
                'message': 'Geçersiz video ID'
            }), 400
        
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Video bilgilerini al
        info = extractor.get_formats(url)
        if not info:
            return jsonify({
                'success': False,
                'message': 'Video bulunamadı veya erişilemiyor'
            }), 404
        
        # Formatları işle
        formats = []
        best_video = None
        best_audio = None
        
        for format_info in info.get('formats', []):
            format_data = {
                'format_id': format_info.get('format_id'),
                'ext': format_info.get('ext'),
                'resolution': format_info.get('resolution', 'N/A'),
                'height': format_info.get('height'),
                'width': format_info.get('width'),
                'filesize': format_info.get('filesize'),
                'filesize_mb': round(format_info.get('filesize', 0) / 1024 / 1024, 1) if format_info.get('filesize') else None,
                'url': format_info.get('url'),
                'format_note': format_info.get('format_note', ''),
                'acodec': format_info.get('acodec'),
                'vcodec': format_info.get('vcodec'),
                'abr': format_info.get('abr'),
                'vbr': format_info.get('vbr'),
                'fps': format_info.get('fps'),
                'tbr': format_info.get('tbr'),
            }
            
            formats.append(format_data)
            
            # En iyi video formatını bul
            if (format_info.get('vcodec') != 'none' and 
                format_info.get('acodec') == 'none' and 
                format_info.get('height')):
                current_height = format_info.get('height')
                if current_height is not None:
                    best_height = best_video.get('height') if best_video else None
                    if not best_video or (best_height is None) or (current_height > best_height):
                        best_video = format_data
            
            # En iyi ses formatını bul
            if (format_info.get('acodec') != 'none' and 
                format_info.get('vcodec') == 'none'):
                current_abr = format_info.get('abr')
                if current_abr is not None:
                    best_abr = best_audio.get('abr') if best_audio else None
                    if not best_audio or (best_abr is None) or (current_abr > best_abr):
                        best_audio = format_data
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'formats': formats,
            'best_formats': {
                'video': best_video,
                'audio': best_audio
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {e}'
        }), 500

@app.route('/video/<video_id>/basic', methods=['GET'])
def get_basic_video_info(video_id):
    """
    Temel video bilgilerini al (formatlar olmadan)
    
    Args:
        video_id (str): YouTube video ID'si
    
    Returns:
    {
        "success": true,
        "video_id": "dQw4w9WgXcQ",
        "title": "Video Başlığı",
        "description": "Video açıklaması",
        "duration": 180,
        "duration_formatted": "3:00",
        "uploader": "Kanal Adı",
        "upload_date": "20231201",
        "view_count": 1234567,
        "like_count": 12345,
        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    }
    """
    try:
        # Video ID'sinin geçerli olup olmadığını kontrol et
        if len(video_id) != 11:
            return jsonify({
                'success': False,
                'message': 'Geçersiz video ID'
            }), 400
        
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Video bilgilerini al
        info = extractor.get_video_info(url)
        if not info:
            return jsonify({
                'success': False,
                'message': 'Video bulunamadı veya erişilemiyor'
            }), 404
        
        # Süreyi formatla
        duration = info.get('duration', 0)
        duration_formatted = f"{duration // 60}:{duration % 60:02d}" if duration else "0:00"
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'title': info.get('title', 'Bilinmiyor'),
            'description': info.get('description', ''),
            'duration': duration,
            'duration_formatted': duration_formatted,
            'uploader': info.get('uploader', 'Bilinmiyor'),
            'upload_date': info.get('upload_date', ''),
            'view_count': info.get('view_count', 0),
            'like_count': info.get('like_count', 0),
            'thumbnail': info.get('thumbnail', '')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {e}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    API sağlık kontrolü
    
    Returns:
    {
        "status": "healthy",
        "message": "YouTube Info API çalışıyor"
    }
    """
    return jsonify({
        'status': 'healthy',
        'message': 'YouTube Info API çalışıyor'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
