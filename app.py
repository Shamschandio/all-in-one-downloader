import streamlit as st
import yt_dlp
from pytubefix import YouTube
import os
import subprocess

st.set_page_config(page_title="SOCIAL EXPERIMENT: FINAL", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT: FINAL")

# --- 1. UI SETUP ---
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

        # --- TIKTOK: FORCING STEREO 256kbps ---
        if "tiktok.com" in url:
            with st.spinner("🚀 EXTRACTING MAX TIKTOK AUDIO..."):
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': 'downloads/%(id)s.%(ext)s',
                    'merge_output_format': 'mp4',
                    'postprocessor_args': [
                        '-c:a', 'aac', '-b:a', '256k', '-ac', '2' # FORCE STEREO 256K
                    ],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    f_path = ydl.prepare_filename(info)
                
                with open(f_path, "rb") as f:
                    st.download_button("💾 DOWNLOAD 4K TIKTOK (STEREO)", f, file_name="tiktok_hd_pro.mp4")

        # --- YOUTUBE: THE "TV" BYPASS ---
        elif "youtube.com" in url or "youtu.be" in url:
            with st.spinner("🕵️ TV-CLIENT HANDSHAKE (BYPASSING 403)..."):
                # 'TV' client is currently the only one YouTube doesn't 403-block on Cloud
                yt = YouTube(url, client='TV')
                
                # Check for cookies in Secrets
                if "YOUTUBE_COOKIES" in st.secrets:
                    with open("temp_cookies.txt", "w") as f:
                        f.write(st.secrets["YOUTUBE_COOKIES"])
                    yt.cookiefile = "temp_cookies.txt"

                st.write(f"📹 **Video:** {yt.title}")

                # Grabbing the BEST available adaptive streams
                v_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
                a_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                if v_stream and a_stream:
                    v_temp = v_stream.download(filename="v_temp.mp4")
                    a_temp = a_stream.download(filename="a_temp.mp4")

                    # FORCE MERGE INTO STEREO
                    output_name = f"yt_hd_{yt.video_id}.mp4"
                    cmd = f'ffmpeg -y -i "{v_temp}" -i "{a_temp}" -c:v copy -c:a aac -b:a 256k -ac 2 "{output_name}"'
                    subprocess.run(cmd, shell=True)

                    with open(output_name, "rb") as f:
                        st.download_button("💾 DOWNLOAD YOUTUBE (256KBPS STEREO)", f, file_name=f"{yt.title}.mp4")
                    st.balloons()

    except Exception as e:
        if "403" in str(e):
            st.error("🚨 403 FORBIDDEN: Streamlit's IP is currently blocked.")
            st.info("The code is correct. To fix this, you MUST go to 'Manage App' -> 'Reboot App' to get a new IP address.")
        else:
            st.error(f"❌ ERROR: {e}")
