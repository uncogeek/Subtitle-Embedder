# 🎬 Subtitle Embedder (Soft-Embed)

A Python tool to embed subtitle files as **soft subtitles** (selectable tracks) into video files. Subtitles are embedded as separate streams that can be toggled on/off in video players like VLC, MPV, or any player that supports embedded subtitles.

## ✨ Features

- ✅ **Soft-embed subtitles** - Not hardcoded/burned into video
- ✅ **Multiple subtitle tracks** - Embed as many subtitle files as needed
- ✅ **Language tagging** - Each subtitle track labeled with language code
- ✅ **Fast processing** - Copies video/audio streams without re-encoding (optional)
- ✅ **Multiple formats** - Supports SRT, ASS, SSA, VTT subtitles
- ✅ **Multiple containers** - Works with MP4, MKV, AVI, MOV

## 📋 Requirements

### 1. Python 3.6+
Check your Python version:
```bash
python --version
# or
python3 --version
```

### 2. FFmpeg
FFmpeg must be installed and accessible from command line.

**Install FFmpeg:**

- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `winget install FFmpeg`
- **Mac:** `brew install ffmpeg`
- **Linux (Ubuntu/Debian):** `sudo apt install ffmpeg`
- **Linux (Fedora):** `sudo dnf install ffmpeg`

**Verify installation:**
```bash
ffmpeg -version
```

## 🚀 Quick Start

### Basic Usage

```bash
# Single subtitle
python subtitle_embedder.py video.mp4 subtitle.srt:eng:English

# Multiple subtitles in ONE LINE (space-separated)
python subtitle_embedder.py video.mp4 english.srt:eng:English persian.srt:fas:Persian arabic.srt:ara:Arabic
```

## 📖 Usage Guide

### Command Syntax

```bash
python subtitle_embedder.py VIDEO_FILE SUBTITLE1 SUBTITLE2 ... [OPTIONS]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `VIDEO_FILE` | Yes | Input video file (MP4, MKV, AVI, MOV) |
| `SUBTITLE(S)` | Yes | One or more subtitle files: `file.srt:lang:title` (space-separated) |
| `-o, --output` | No | Custom output filename (default: `input_subtitled.ext`) |
| `--no-copy-video` | No | Re-encode video instead of copying (slower but more compatible) |
| `--no-copy-audio` | No | Re-encode audio instead of copying |

### Subtitle Format: `file:language:title`

- **file** - Path to subtitle file (required)
- **language** - ISO 639-2 language code (optional, defaults to 'und')
- **title** - Display name for the track (optional, defaults to filename)

## 📝 Examples

### Example 1: Single Subtitle
```bash
python subtitle_embedder.py movie.mp4 subtitles.srt:eng:English
```

### Example 2: Multiple Languages (ONE-LINE!)
```bash
python subtitle_embedder.py movie.mp4 english.srt:eng:English persian.srt:fas:Persian arabic.srt:ara:Arabic
```

### Example 3: Custom Output Path
```bash
python subtitle_embedder.py movie.mp4 subtitles.srt:eng:English -o "movie_with_subs.mp4"
```

### Example 4: Only Language Code (title auto-detected)
```bash
python subtitle_embedder.py movie.mp4 english.srt:eng persian.srt:fas
```

### Example 5: Multiple Subtitles with Short Format
```bash
python subtitle_embedder.py movie.mp4 en.srt:eng fa.srt:fas ar.srt:ara tr.srt:tur
```

### Example 6: Re-encode for Maximum Compatibility
```bash
python subtitle_embedder.py movie.mp4 subtitles.srt:eng --no-copy-video --no-copy-audio
```
*Note: This is much slower but ensures maximum compatibility*

## 🌍 Common Language Codes (ISO 639-2)

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | `eng` | Persian | `fas` |
| Arabic | `ara` | Turkish | `tur` |
| Spanish | `spa` | French | `fra` |
| German | `deu` | Italian | `ita` |
| Portuguese | `por` | Japanese | `jpn` |
| Korean | `kor` | Chinese | `zho` |
| Russian | `rus` | Hindi | `hin` |
| Dutch | `nld` | Polish | `pol` |
| Swedish | `swe` | Norwegian | `nor` |
| Danish | `dan` | | |

[Full list of ISO 639-2 codes](https://www.loc.gov/standards/iso639-2/php/code_list.php)

## 🎯 Supported Formats

### Video Formats
- MP4 (`.mp4`, `.m4v`)
- Matroska (`.mkv`)
- AVI (`.avi`)
- QuickTime (`.mov`)

### Subtitle Formats
- SubRip (`.srt`)
- Advanced SubStation Alpha (`.ass`)
- SubStation Alpha (`.ssa`)
- WebVTT (`.vtt`)

## 💡 Tips & Best Practices

### 1. **Use Copy Mode (Default)**
By default, video and audio streams are copied without re-encoding. This is:
- ⚡ **Much faster** (seconds instead of minutes)
- 📼 **Lossless** (no quality loss)
- 💾 **Smaller files** (no additional compression)

### 2. **When to Re-encode**
Use `--no-copy-video` if:
- Output file doesn't play correctly
- You need a specific codec
- You want to compress the video further

### 3. **Subtitle Naming Convention**
For best organization:
```
movie.mp4
movie.eng.srt
movie.spa.srt
movie.fra.srt
```

### 4. **Testing Subtitles**
After embedding, test in multiple players:
- **VLC Media Player** - Press `V` to cycle through subtitles
- **MPV** - Press `J` to cycle through subtitles
- **Windows Media Player** - Right-click → Lyrics, captions, and subtitles

### 5. **Batch Processing**
For multiple videos, use a shell script:

**Bash (Linux/Mac):**
```bash
#!/bin/bash
for video in *.mp4; do
  python subtitle_embedder.py "$video" "${video%.mp4}.eng.srt:eng:English" "${video%.mp4}.fas.srt:fas:Persian" "${video%.mp4}.ara.srt:ara:Arabic"
done
```

**PowerShell (Windows):**
```powershell
Get-ChildItem *.mp4 | ForEach-Object {
  $base = $_.BaseName
  python subtitle_embedder.py $_.Name "$base.eng.srt:eng:English" "$base.fas.srt:fas:Persian" "$base.ara.srt:ara:Arabic"
}
```

## 🔧 Troubleshooting

### Problem: "FFmpeg is not installed"
**Solution:** Install FFmpeg and ensure it's in your system PATH.

### Problem: "Subtitle file not found"
**Solution:** Check the file path and ensure the subtitle file exists.

### Problem: Subtitles don't display in player
**Solution:** 
- Ensure your player supports embedded subtitles
- Try VLC (most compatible)
- Check subtitle format is supported
- Try re-encoding: `--no-copy-video`

### Problem: Output file is very large
**Solution:** 
- Default copy mode should keep file size similar
- If much larger, your original video was highly compressed
- Use `--no-copy-video` to compress further (slower)

### Problem: "Unsupported subtitle format"
**Solution:** Convert subtitle to SRT format using online converters or:
```bash
ffmpeg -i input.sub -o output.srt
```

## 📂 Project Structure

```
subtitle-embedder/
├── subtitle_embedder.py    # Main script
├── README.md               # This file
└── examples/              # Example files (optional)
    ├── sample_video.mp4
    └── sample_subtitle.srt
```

## 🎓 How It Works

1. **Input Validation** - Checks video and subtitle files exist and are supported formats
2. **FFmpeg Command Building** - Constructs appropriate FFmpeg command with:
   - Video input mapping
   - Multiple subtitle input mappings
   - Codec selection (copy or re-encode)
   - Metadata tags (language codes, titles)
3. **Processing** - Executes FFmpeg to mux subtitles into video container
4. **Output** - Creates new video file with embedded subtitle tracks

## 🤝 Contributing

Suggestions and improvements are welcome! Some ideas:
- Auto-detect subtitle files in same folder
- GUI interface
- Drag-and-drop functionality
- Preset profiles for different use cases

## 📄 License

This tool is provided as-is for personal and educational use. FFmpeg is licensed under LGPL/GPL.

## 🙏 Credits

- Built with Python and FFmpeg
- Uses FFmpeg for video processing
- Follows ISO 639-2 language code standards

---

**Made with ❤️ for subtitle enthusiasts**

*For issues or questions, please check FFmpeg documentation or subtitle format specifications.*
