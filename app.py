import streamlit as st
import yt_dlp
import os

# App interface settings
st.set_page_config(page_title="Bootyra 4K Downloader", page_icon="🎬")
st.title("🎬 Bootyra 4K Video Downloader")
st.info("Paste a link below. This app uses cookies to bypass restrictions.")

# Create downloads folder if it doesn't exist
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("Video URL:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # Configuration for yt-dlp
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',  # This file must exist in your GitHub repo
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
        }

        with st.spinner("Downloading... please wait."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info and download
                info = ydl.extract_info(url, download=True)
                # Determine the final filename
                file_path = ydl.prepare_filename(info)
                
                # Double check extension (merging often results in .mp4)
                if not os.path.exists(file_path):
                    base = os.path.splitext(file_path)[0]
                    file_path = base + ".mp4"

        st.success(f"Successfully downloaded: {info.get('title')}")

        # Provide the download button
        with open(file_path, "rb") as f:
            st.download_button(
                label="💾 Save Video to Device",
                data=f,
                file_name=os.path.basename(file_path),
                mime="video/mp4"
            )

    except Exception as e:
        st.error(f"Error: {e}")
        st.warning("Make sure your cookies.txt is up to date in GitHub!")

# Custom Sidebar
with st.sidebar:
    st.title("Settings")
    st.write("Mode: Private/Invite-Only")
    st.write("Engine: yt-dlp + FFmpeg")