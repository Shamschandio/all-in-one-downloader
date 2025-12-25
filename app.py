import streamlit as st
import yt_dlp
import os

# Create a downloads folder if it doesn't exist
if not os.path.exists("downloads"):
    os.makedirs("downloads")

def download_media(url):
    save_path = 'downloads/%(title)s.%(ext)s'
    
    ydl_opts = {
        # 'best' ensures we get the highest res, and we force mp4 for compatibility
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': save_path,
        # This argument is key for TikTok no-watermark
        'extractor_args': {'tiktok': {'web_api': True}},
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

st.set_page_config(page_title="MediaX Ultra", page_icon="🚀")
st.title("🚀 MediaX: 4K & No-Watermark Downloader")
st.markdown("Works for **TikTok** (No Watermark), **YouTube** (4K), and **Instagram**.")

url = st.text_input("Paste your link here:", placeholder="https://...")

if st.button("Process Video"):
    if url:
        with st.spinner("Fetching best quality... this may take a minute for 4K."):
            try:
                # 1. Download to server/computer
                file_path = download_media(url)
                
                # 2. Read the file into memory so the user can save it
                with open(file_path, "rb") as f:
                    video_bytes = f.read()
                    
                st.success("Video processed successfully!")
                
                # 3. Show the actual save button
                st.download_button(
                    label="💾 Save Video to Device",
                    data=video_bytes,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4"
                )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a URL first.")