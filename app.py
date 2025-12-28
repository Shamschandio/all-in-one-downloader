import streamlit as st
import yt_dlp
from pytubefix import YouTube
import os
from moviepy.editor import VideoFileClip, AudioFileClip

# --- PAGE SETUP ---
st.set_page_config(page_title="SOCIAL EXPERIMENT: HD PRO", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT: HD PRO")

# --- COOKIE HANDLING (For YouTube Login Error) ---
cookie_path = "youtube_cookies.txt"
if "YOUTUBE_COOKIES" in st.secrets:
    with open(cookie_path, "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

# --- SESSION STATE ---
if 'url_input' not in st.session_state:
    st.session_state.url_input = ""

def clear_text():
    st.session_state.url_input = ""

url = st.text_input("PASTE LINK HERE:", key="url_input")

col1, col2 = st.columns([1, 5])
with col1:
    submit = st.button("🚀 GO")
with col2:
    st.button("🗑️ CLEAR", on_click=clear_text)

if submit and url:
    try:
        # --- TIKTOK (Best Quality & Bitrate) ---
        if "tiktok.com" in url:
            with st.spinner("🚀 FETCHING TIKTOK (MAX BITRATE)..."):
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best', # Force merge best video + best stereo audio
                    'outtmpl': 'downloads/%(id)s.%(ext)s',
                    'merge_output_format': 'mp4',
                    'quiet': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info)
                
                with open(file_path, "rb") as f:
                    st.download_button("💾 DOWNLOAD HD TIKTOK", f, file_name="tiktok_hd.mp4")

        # --- YOUTUBE (High-Res + Stereo Audio Merger) ---
        elif "youtube.com" in url or "youtu.be" in url:
            with st.spinner("🕵️ BYPASSING LOGIN & PREPARING HD..."):
                # Use the cookie file if it exists to fix the 'Login Required' error
                yt = YouTube(url, use_oauth=False, cookiefile=cookie_path if os.path.exists(cookie_path) else None)
                
                st.write(f"📹 **Title:** {yt.title}")

                # 1. Download Highest Quality Video (No Audio)
                video_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
                # 2. Download Highest Quality Audio (Stereo, 128kbps+)
                audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                if video_stream and audio_stream:
                    v_file = video_stream.download(filename="video_temp.mp4")
                    a_file = audio_stream.download(filename="audio_temp.mp3")

                    st.info(f"Merging Video ({video_stream.resolution}) + Stereo Audio ({audio_stream.abr})...")

                    # 3. Use MoviePy to merge them
                    video_clip = VideoFileClip(v_file)
                    audio_clip = AudioFileClip(a_file)
                    final_clip = video_clip.set_audio(audio_clip)
                    final_clip.write_videofile("final_output.mp4", codec="libx264", audio_codec="aac")

                    with open("final_output.mp4", "rb") as f:
                        st.download_button("💾 DOWNLOAD FULL HD (STEREO)", f, file_name=f"{yt.title}.mp4")
                    st.balloons()
                
    except Exception as e:
        st.error(f"❌ ERROR: {e}")

# Cleanup
if os.path.exists(cookie_path):
    os.remove(cookie_path)
