import streamlit as st
from pytubefix import YouTube
import yt_dlp
import os
import shutil

# --- 1. SETUP & BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K")
st.markdown("---")

# Create a clean downloads folder
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("PASTE LINK (YOUTUBE OR TIKTOK):", placeholder="https://...")

if url:
    try:
        # --- TIKTOK ENGINE (using yt-dlp) ---
        if "tiktok.com" in url:
            with st.spinner("🚀 BYPASSING TIKTOK..."):
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': 'downloads/%(id)s.%(ext)s',
                    'nocheckcertificate': True,
                    'quiet': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info)
                
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button("💾 DOWNLOAD TIKTOK VIDEO", f, file_name=os.path.basename(file_path))
                    st.success("TIKTOK READY!")

        # --- YOUTUBE ENGINE (using pytubefix + iOS Stealth) ---
        elif "youtube.com" in url or "youtu.be" in url:
            with st.spinner("🕵️ YOUTUBE STEALTH MODE..."):
                # 'client=IOS' is the current strongest bypass for 403 errors
                yt = YouTube(url, client='IOS')
                
                st.subheader(f"📹 {yt.title}")
                
                # Get the highest resolution MP4 (Progressive)
                video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
                
                if video:
                    st.info(f"Resolution: {video.resolution} | Size: {round(video.filesize_mb, 2)} MB")
                    
                    # Download to local folder
                    out_path = video.download(output_path="downloads")
                    
                    with open(out_path, "rb") as f:
                        st.download_button("💾 DOWNLOAD YOUTUBE VIDEO", f, file_name=os.path.basename(out_path))
                    st.balloons()
                else:
                    st.error("No compatible MP4 found. This video might be restricted.")

        else:
            st.warning("⚠️ Please enter a valid YouTube or TikTok link.")

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
        if "403" in str(e):
            st.warning("🚨 IP BLOCK DETECTED. Please go to 'Manage App' -> 'Reboot' to get a fresh IP address.")

# --- CLEANUP (Optional) ---
if st.button("🗑️ Clear Cache"):
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
        os.makedirs("downloads")
    st.success("Cache Cleared!")
