import streamlit as st
import yt_dlp
from pytubefix import YouTube
import os
import subprocess

# --- PAGE SETUP ---
st.set_page_config(page_title="SOCIAL EXPERIMENT: ULTIMATE", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT: ULTIMATE")

# --- 1. THE COOKIE FIX ---
# Instead of a file path, pytubefix 2025 often prefers the 'WEB' client 
# with cookies passed via the internal 'pointer'.
cookie_path = "cookies.txt"
if "YOUTUBE_COOKIES" in st.secrets:
    with open(cookie_path, "w") as f:
        f.write(st.secrets["YOUTUBE_COOKIES"])

# --- 2. UI ---
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
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        # --- TIKTOK SECTION ---
        if "tiktok.com" in url:
            with st.spinner("🚀 FETCHING TIKTOK HD (STEREO)..."):
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best', # This forces the best stereo audio
                    'outtmpl': 'downloads/%(id)s.%(ext)s',
                    'merge_output_format': 'mp4',
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    f_path = ydl.prepare_filename(info)
                
                with open(f_path, "rb") as f:
                    st.download_button("💾 DOWNLOAD HD TIKTOK", f, file_name="tiktok_hd.mp4")

        # --- YOUTUBE SECTION ---
        elif "youtube.com" in url or "youtu.be" in url:
            with st.spinner("🕵️ BYPASSING LOGIN & MERGING HD AUDIO..."):
                # FIX: We use 'cookiefile' as a standalone parameter in the NEW pytubefix way
                yt = YouTube(url, use_oauth=False)
                # We manually inject the cookiefile path into the request handle
                yt.cookiefile = cookie_path if os.path.exists(cookie_path) else None
                
                st.write(f"📹 **Video:** {yt.title}")

                # SELECT HIGHEST ADAPTIVE STREAMS (This is how you get Stereo + 1080p+)
                # We avoid 'progressive=True' because it's always low quality
                v_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
                a_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                if v_stream and a_stream:
                    st.write(f"💎 Audio Quality: {a_stream.abr} (Stereo)")
                    
                    v_file = v_stream.download(filename="v_temp.mp4")
                    a_file = a_stream.download(filename="a_temp.mp4")

                    # --- FFmpeg MERGE (The Stereo Glue) ---
                    output_name = f"final_{yt.video_id}.mp4"
                    # -map 0:v:0 grabs first video, -map 1:a:0 grabs first audio
                    cmd = f'ffmpeg -y -i "{v_file}" -i "{a_file}" -c:v copy -c:a aac -b:a 192k "{output_name}"'
                    subprocess.run(cmd, shell=True)

                    with open(output_name, "rb") as f:
                        st.download_button("💾 DOWNLOAD FULL HD (STEREO 192kbps)", f, file_name=f"{yt.title}.mp4")
                    st.balloons()

    except Exception as e:
        st.error(f"❌ ERROR: {e}")

# Cleanup
if os.path.exists(cookie_path):
    os.remove(cookie_path)
