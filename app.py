import streamlit as st
import yt_dlp
from pytubefix import YouTube
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="SOCIAL EXPERIMENT PRO", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT: ALL-IN-ONE")
st.markdown("---")

if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("PASTE YOUTUBE OR TIKTOK LINK:", placeholder="https://...")

if url:
    try:
        # --- ENGINE 1: TIKTOK (The working method) ---
        if "tiktok.com" in url:
            with st.spinner("⚡ FETCHING TIKTOK HD..."):
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': 'downloads/%(id)s.%(ext)s',
                    'quiet': True,
                    'nocheckcertificate': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    }
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info)
                
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button("💾 DOWNLOAD TIKTOK (MP4)", f, file_name=os.path.basename(file_path))
                    st.success("TIKTOK READY")

        # --- ENGINE 2: YOUTUBE (The Stealth Method) ---
        elif "youtube.com" in url or "youtu.be" in url:
            with st.spinner("🕵️ YOUTUBE STEALTH HANDSHAKE..."):
                # We use the 'MWEB' (Mobile Web) client. 
                # In late 2025, this is often the most stable for cloud servers.
                yt = YouTube(url, client='MWEB')
                
                st.subheader(f"📹 {yt.title}")
                
                # Get the best 'Progressive' stream (Video + Audio combined)
                video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
                
                if video:
                    st.info(f"Resolution: {video.resolution} | Size: {round(video.filesize_mb, 2)} MB")
                    path = video.download(output_path="downloads")
                    
                    with open(path, "rb") as f:
                        st.download_button("💾 DOWNLOAD YOUTUBE (MP4)", f, file_name=os.path.basename(path))
                    st.balloons()
                else:
                    st.error("No compatible MP4 found. Try another video or check back later.")

    except Exception as e:
        if "403" in str(e):
            st.error("🚨 YOUTUBE IP BLOCK: Streamlit's server IP is currently restricted by YouTube.")
            st.info("Try clicking 'Reboot App' in the Manage App menu to get a fresh IP.")
        else:
            st.error(f"❌ ERROR: {e}")

# --- SIDEBAR TOOLS ---
with st.sidebar:
    st.header("Settings")
    if st.button("🗑️ Clear Server Cache"):
        for f in os.listdir("downloads"):
            os.remove(os.path.join("downloads", f))
        st.success("Cleaned!")
