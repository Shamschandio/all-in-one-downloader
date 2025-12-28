import streamlit as st
import yt_dlp
from pytubefix import YouTube
import os
import subprocess

# --- PAGE SETUP ---
st.set_page_config(page_title="SOCIAL EXPERIMENT: HD PRO", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT: HD PRO")

# --- COOKIE HANDLING ---
cookie_path = "youtube_cookies.txt"
if "YOUTUBE_COOKIES" in st.secrets:
    with open(cookie_path, "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

# --- UI LAYOUT ---
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
        # Create unique folder for this download
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        # --- TIKTOK (High Bitrate) ---
        if "tiktok.com" in url:
            with st.spinner("🚀 FETCHING TIKTOK HD..."):
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': 'downloads/%(id)s.%(ext)s',
                    'merge_output_format': 'mp4',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    f_path = ydl.prepare_filename(info)
                
                with open(f_path, "rb") as f:
                    st.download_button("💾 DOWNLOAD HD TIKTOK", f, file_name="tiktok_hd.mp4")

        # --- YOUTUBE (Stereo + 1080p/4K Merger) ---
        elif "youtube.com" in url or "youtu.be" in url:
            with st.spinner("🕵️ EXTRACTING HD STREAMS..."):
                yt = YouTube(url, use_oauth=False, cookiefile=cookie_path if os.path.exists(cookie_path) else None)
                
                # Get Best Video (No Audio) & Best Audio (Stereo)
                v_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
                a_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                if v_stream and a_stream:
                    v_file = v_stream.download(filename="v_temp.mp4")
                    a_file = a_stream.download(filename="a_temp.mp4")

                    st.info(f"Merging: {v_stream.resolution} Video + {a_stream.abr} Stereo Audio")
                    
                    # --- THE PRO MERGER (Direct FFmpeg) ---
                    # This is much faster than MoviePy and doesn't crash
                    output_name = "final_hd_video.mp4"
                    cmd = f'ffmpeg -y -i "{v_file}" -i "{a_file}" -c copy -map 0:v:0 -map 1:a:0 "{output_name}"'
                    subprocess.run(cmd, shell=True)

                    with open(output_name, "rb") as f:
                        st.download_button("💾 DOWNLOAD FULL HD (STEREO)", f, file_name=f"{yt.title}.mp4")
                    st.balloons()

    except Exception as e:
        st.error(f"❌ ERROR: {e}")

# Cleanup
if os.path.exists(cookie_path):
    os.remove(cookie_path)
