#!/usr/bin/env python3
"""
Subtitle Embedder - Soft-embed subtitles into MP4 videos
Embeds subtitle files as selectable tracks (not hardcoded/burned)
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional

class SubtitleEmbedder:
    """Handle soft-embedding of subtitles into video files using FFmpeg"""
    
    SUPPORTED_VIDEO_FORMATS = {'.mp4', '.mkv', '.avi', '.mov', '.m4v'}
    SUPPORTED_SUBTITLE_FORMATS = {'.srt', '.ass', '.ssa', '.vtt'}
    
    def __init__(self):
        self.check_ffmpeg()
    
    def check_ffmpeg(self) -> bool:
        """Check if FFmpeg is installed and accessible"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ERROR: FFmpeg is not installed or not in PATH")
            print("Please install FFmpeg: https://ffmpeg.org/download.html")
            sys.exit(1)
    
    def validate_file(self, filepath: str, file_type: str) -> Path:
        """Validate file exists and has correct extension"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"{file_type} file not found: {filepath}")
        
        if file_type == "video":
            if path.suffix.lower() not in self.SUPPORTED_VIDEO_FORMATS:
                raise ValueError(f"Unsupported video format: {path.suffix}")
        elif file_type == "subtitle":
            if path.suffix.lower() not in self.SUPPORTED_SUBTITLE_FORMATS:
                raise ValueError(f"Unsupported subtitle format: {path.suffix}")
        
        return path
    
    def embed_subtitles(self, 
                       video_path: str,
                       subtitle_tracks: List[Dict[str, str]],
                       output_path: Optional[str] = None,
                       copy_video: bool = True,
                       copy_audio: bool = True) -> bool:
        """
        Embed multiple subtitle tracks into a video file
        
        Args:
            video_path: Path to input video file
            subtitle_tracks: List of dicts with 'file', 'language', and optional 'title'
            output_path: Path for output file (default: adds '_subtitled' suffix)
            copy_video: Copy video stream without re-encoding (faster)
            copy_audio: Copy audio stream without re-encoding (faster)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate input video
            video = self.validate_file(video_path, "video")
            
            # Validate subtitle files
            for track in subtitle_tracks:
                self.validate_file(track['file'], "subtitle")
            
            # Generate output path if not provided
            if output_path is None:
                output_path = video.parent / f"{video.stem}_subtitled{video.suffix}"
            else:
                output_path = Path(output_path)
            
            # Build FFmpeg command
            cmd = ['ffmpeg', '-i', str(video)]
            
            # Add subtitle inputs
            for track in subtitle_tracks:
                cmd.extend(['-i', track['file']])
            
            # Map video stream
            cmd.extend(['-map', '0:v'])
            
            # Map audio streams (all of them)
            cmd.extend(['-map', '0:a?'])
            
            # Map subtitle streams
            for i in range(len(subtitle_tracks)):
                cmd.extend(['-map', f'{i+1}:s'])
            
            # Video codec
            if copy_video:
                cmd.extend(['-c:v', 'copy'])
            else:
                cmd.extend(['-c:v', 'libx264'])
            
            # Audio codec
            if copy_audio:
                cmd.extend(['-c:a', 'copy'])
            else:
                cmd.extend(['-c:a', 'aac'])
            
            # Subtitle codec (mov_text for MP4, copy for MKV)
            if video.suffix.lower() == '.mp4':
                cmd.extend(['-c:s', 'mov_text'])
            else:
                cmd.extend(['-c:s', 'copy'])
            
            # Add metadata for each subtitle track
            for i, track in enumerate(subtitle_tracks):
                lang = track.get('language', 'und')
                title = track.get('title', '')
                
                cmd.extend([f'-metadata:s:s:{i}', f'language={lang}'])
                if title:
                    cmd.extend([f'-metadata:s:s:{i}', f'title={title}'])
            
            # Output file
            cmd.append(str(output_path))
            
            # Show command
            print(f"\n🎬 Embedding subtitles into: {video.name}")
            print(f"📝 Subtitle tracks: {len(subtitle_tracks)}")
            for i, track in enumerate(subtitle_tracks, 1):
                lang = track.get('language', 'und')
                title = track.get('title', Path(track['file']).stem)
                print(f"   {i}. {title} [{lang}]")
            print(f"💾 Output: {output_path.name}\n")
            
            # Execute FFmpeg
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode == 0:
                print(f"✅ Success! Subtitles embedded successfully.")
                print(f"📁 Output saved to: {output_path}")
                return True
            else:
                print(f"❌ Error during embedding:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

def parse_subtitle_arg(arg: str) -> Dict[str, str]:
    """
    Parse subtitle argument in format: file.srt:eng:English
    or file.srt:eng
    or just file.srt
    """
    parts = arg.split(':')
    result = {'file': parts[0]}
    
    if len(parts) > 1:
        result['language'] = parts[1]
    else:
        result['language'] = 'und'  # undefined
    
    if len(parts) > 2:
        result['title'] = ':'.join(parts[2:])  # Join back in case title has colons
    else:
        result['title'] = Path(parts[0]).stem
    
    return result

def main():
    parser = argparse.ArgumentParser(
        description='Embed subtitle files as soft subtitles into video files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Single subtitle
  python subtitle_embedder.py video.mp4 subtitle.srt:eng:English
  
  # Multiple subtitles (one-line, space-separated)
  python subtitle_embedder.py video.mp4 english.srt:eng:English spanish.srt:spa:Spanish
  
  # With custom output
  python subtitle_embedder.py video.mp4 sub.srt:eng:English -o output.mp4
  
  # Re-encode video (slower but more compatible)
  python subtitle_embedder.py video.mp4 sub.srt:eng --no-copy-video

Language codes (ISO 639-2):
  eng - English    spa - Spanish    fra - French
  deu - German     ita - Italian    por - Portuguese
  jpn - Japanese   kor - Korean     zho - Chinese
  ara - Arabic     rus - Russian    hin - Hindi
        '''
    )
    
    parser.add_argument('video', help='Input video file (MP4, MKV, AVI, MOV)')
    parser.add_argument('subtitles',
                       nargs='+',
                       help='Subtitle files in format: file.srt:lang:title (space-separated)')
    parser.add_argument('-o', '--output',
                       help='Output video file (default: input_subtitled.ext)')
    parser.add_argument('--no-copy-video',
                       action='store_false',
                       dest='copy_video',
                       help='Re-encode video instead of copying (slower)')
    parser.add_argument('--no-copy-audio',
                       action='store_false',
                       dest='copy_audio',
                       help='Re-encode audio instead of copying')
    
    args = parser.parse_args()
    
    # Parse subtitle arguments
    subtitle_tracks = [parse_subtitle_arg(s) for s in args.subtitles]
    
    # Create embedder and process
    embedder = SubtitleEmbedder()
    success = embedder.embed_subtitles(
        video_path=args.video,
        subtitle_tracks=subtitle_tracks,
        output_path=args.output,
        copy_video=args.copy_video,
        copy_audio=args.copy_audio
    )
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()