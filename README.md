# YouTube Video Info API

YouTube video ID'si alıp video bilgilerini ve indirme linklerini döndüren Flask API'si. Mobil uygulamalar için backend servisi.

## 🚀 Özellikler

- **Video Bilgileri**: Başlık, açıklama, süre, kanal bilgileri
- **Format Listesi**: Tüm mevcut video ve ses formatları
- **İndirme Linkleri**: Doğrudan indirme URL'leri
- **En İyi Formatlar**: Otomatik en iyi video ve ses formatı seçimi
- **RESTful API**: JSON tabanlı API endpoints
- **CORS Desteği**: Cross-origin istekleri destekler
- **Hızlı Yanıt**: Sadece bilgi çıkarma, indirme yok

## 📋 Gereksinimler

- Python 3.7+
- yt-dlp
- Flask
- Flask-CORS

## 🛠️ Kurulum

1. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

2. **API'yi başlatın:**
```bash
python app.py
```

API varsayılan olarak `http://localhost:5000` adresinde çalışır.

## 📡 API Endpoints

### 1. Sağlık Kontrolü
```http
GET /health
```

**Yanıt:**
```json
{
  "status": "healthy",
  "message": "YouTube Info API çalışıyor"
}
```

### 2. Tam Video Bilgileri
```http
GET /video/{video_id}
```

**Yanıt:**
```json
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
      "format_note": "4K",
      "acodec": "none",
      "vcodec": "avc1.640032",
      "fps": 30
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
```

### 3. Sadece Formatlar
```http
GET /video/{video_id}/formats
```

**Yanıt:**
```json
{
  "success": true,
  "video_id": "dQw4w9WgXcQ",
  "formats": [...],
  "best_formats": {
    "video": {...},
    "audio": {...}
  }
}
```

### 4. Temel Bilgiler
```http
GET /video/{video_id}/basic
```

**Yanıt:**
```json
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
```

## 📊 Format Bilgileri

Her format şu bilgileri içerir:

- `format_id`: YouTube format ID'si
- `ext`: Dosya uzantısı (mp4, webm, m4a, vb.)
- `resolution`: Çözünürlük (1920x1080, vb.)
- `height`: Yükseklik (piksel)
- `width`: Genişlik (piksel)
- `filesize`: Dosya boyutu (byte)
- `filesize_mb`: Dosya boyutu (MB)
- `url`: Doğrudan indirme linki
- `format_note`: Format açıklaması (4K, 1080p, vb.)
- `acodec`: Ses codec'i
- `vcodec`: Video codec'i
- `abr`: Ses bitrate'i (kbps)
- `vbr`: Video bitrate'i (kbps)
- `fps`: FPS (kare hızı)
- `tbr`: Toplam bitrate (kbps)

## 🔧 Kullanım Örnekleri

### cURL ile Test

```bash
# Sağlık kontrolü
curl -X GET http://localhost:5000/health

# Tam video bilgileri
curl -X GET http://localhost:5000/video/dQw4w9WgXcQ

# Sadece formatlar
curl -X GET http://localhost:5000/video/dQw4w9WgXcQ/formats

# Temel bilgiler
curl -X GET http://localhost:5000/video/dQw4w9WgXcQ/basic
```

### PowerShell ile Test

```powershell
# Sağlık kontrolü
Invoke-WebRequest -Uri "http://localhost:5000/health" -Method GET

# Tam video bilgileri
Invoke-WebRequest -Uri "http://localhost:5000/video/dQw4w9WgXcQ" -Method GET

# Sadece formatlar
Invoke-WebRequest -Uri "http://localhost:5000/video/dQw4w9WgXcQ/formats" -Method GET
```

### JavaScript ile Test

```javascript
// Tam video bilgileri
fetch('http://localhost:5000/video/dQw4w9WgXcQ')
.then(response => response.json())
.then(data => {
    console.log('Video başlığı:', data.title);
    console.log('En iyi video formatı:', data.best_formats.video);
    console.log('En iyi ses formatı:', data.best_formats.audio);
    
    // İndirme linklerini kullan
    const videoUrl = data.best_formats.video.url;
    const audioUrl = data.best_formats.audio.url;
});

// Sadece formatlar
fetch('http://localhost:5000/video/dQw4w9WgXcQ/formats')
.then(response => response.json())
.then(data => {
    console.log('Tüm formatlar:', data.formats);
});
```

### Android/Kotlin Örneği

```kotlin
// Video bilgilerini al
val response = client.get("http://localhost:5000/video/dQw4w9WgXcQ")
val videoInfo = response.body<VideoInfo>()

// En iyi formatları kullan
val videoUrl = videoInfo.bestFormats.video.url
val audioUrl = videoInfo.bestFormats.audio.url

// İndirme işlemini başlat
downloadManager.enqueue(
    DownloadManager.Request(Uri.parse(videoUrl))
        .setTitle(videoInfo.title)
        .setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, "${videoInfo.title}.mp4")
)
```

## 📁 Dosya Yapısı

```
downloaderBack/
├── app.py                 # Flask API ana dosyası
├── youtube_downloader.py  # Komut satırı indirici (eski)
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Bu dosya
└── downloads/            # İndirilen videolar (eski)
```

## ⚙️ Konfigürasyon

API ayarlarını değiştirmek için `app.py` dosyasındaki değişkenleri düzenleyebilirsiniz:

- `port`: API portu (varsayılan: 5000)
- `host`: API host adresi (varsayılan: "0.0.0.0")

## 🔒 Güvenlik

- API CORS desteği ile tüm origin'lerden gelen istekleri kabul eder
- Production ortamında güvenlik önlemleri eklenmelidir
- Rate limiting ve authentication eklenebilir

## 🐛 Sorun Giderme

### SSL Sertifika Hatası
API SSL sertifika doğrulamasını devre dışı bırakır. Bu normal bir durumdur.

### Video Bulunamıyor
- Video ID'sinin doğru olduğundan emin olun (11 karakter)
- Video'nun erişilebilir olduğunu kontrol edin
- API loglarını kontrol edin

### Format URL'leri Geçersiz
YouTube format URL'leri kısa süreli olabilir. İndirme işlemini hemen yapın.

## 📱 Mobil Uygulama Entegrasyonu

### Android Örneği

```kotlin
data class VideoInfo(
    val success: Boolean,
    val videoId: String,
    val title: String,
    val duration: Int,
    val formats: List<Format>,
    val bestFormats: BestFormats
)

data class Format(
    val formatId: String,
    val ext: String,
    val resolution: String,
    val height: Int?,
    val width: Int?,
    val filesize: Long?,
    val filesizeMb: Double?,
    val url: String,
    val formatNote: String
)

data class BestFormats(
    val video: Format?,
    val audio: Format?
)
```

### iOS Örneği

```swift
struct VideoInfo: Codable {
    let success: Bool
    let videoId: String
    let title: String
    let duration: Int
    let formats: [Format]
    let bestFormats: BestFormats
}

struct Format: Codable {
    let formatId: String
    let ext: String
    let resolution: String
    let height: Int?
    let width: Int?
    let filesize: Int64?
    let filesizeMb: Double?
    let url: String
    let formatNote: String
}

struct BestFormats: Codable {
    let video: Format?
    let audio: Format?
}
```

## 📝 Lisans

Bu proje eğitim amaçlıdır. YouTube'un kullanım şartlarına uygun kullanın.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun
