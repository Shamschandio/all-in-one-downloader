import streamlit as st
import yt_dlp
from pytubefix import YouTube
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="SOCIAL EXPERIMENT PRO", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT: FINAL REPAIR")

# --- SESSION STATE FOR CLEAR BUTTON ---
if 'url_input' not in st.session_state:
    st.session_state.url_input = ""

def clear_text():
    st.session_state.url_input = ""

# --- UI LAYOUT ---
# We use columns to put the "Submit" and "Clear" buttons side-by-side
url = st.text_input("PASTE LINK HERE:", key="url_input")

col1, col2 = st.columns([1, 5])
with col1:
    submit_button = st.button("🚀 GO")
with col2:
    st.button("🗑️ CLEAR LINK", on_click=clear_text)

st.markdown("---")

if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Trigger processing if the button is clicked OR if they press enter
if submit_button and url:
    try:
        # --- TIKTOK REPAIR ---
        if "tiktok.com" in url:
            with st.spinner("🚀 FETCHING TIKTOK..."):
                ydl_opts = {
                    'format': 'best[ext=mp4]/best', 
                    'outtmpl': 'downloads/%(id)s.%(ext)s',
                    'nocheckcertificate': True,
                    'quiet': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    }
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info)
                
                file_size = os.path.getsize(file_path) / 1024
                if file_size < 100:
                    st.error(f"⚠️ Corrupted file ({int(file_size)}KB). TikTok is blocking this specific video.")
                else:
                    with open(file_path, "rb") as f:
                        st.download_button("💾 DOWNLOAD TIKTOK (MP4)", f, file_name=os.path.basename(file_path))
                    st.success(f"READY! {round(file_size/1024, 2)} MB")

        # --- YOUTUBE REPAIR ---
        elif "youtube.com" in url or "youtu.be" in url:
            with st.spinner("🕵️ YOUTUBE ANDROID BYPASS..."):
                yt = YouTube(url, client='ANDROID_MUSIC')
                st.subheader(f"📹 {yt.title}")
                video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
                
                if video:
                    path = video.download(output_path="downloads")
                    with open(path, "rb") as f:
                        st.download_button("💾 DOWNLOAD YOUTUBE", f, file_name=os.path.basename(path))
                    st.balloons()
                else:
                    st.error("YouTube is hiding the MP4 files for this video.")

    except Exception as e:
        if "403" in str(e):
            st.error("🚨 YOUTUBE IP BLOCK: Please 'Reboot App' in the Streamlit menu.")
        else:
            st.error(f"❌ ERROR: {e}")

elif submit_button and not url:
    st.warning("Please paste a link first!")
