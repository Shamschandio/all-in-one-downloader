import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. APP CONFIG ---
st.set_page_config(page_title="Universal Downloader", page_icon="🚀")
st.title("🚀 Universal Video Downloader")

# --- 2. COOKIE LOADER ---
cookie_file_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    temp_cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w')
    temp_cookie_file.write(st.secrets["YOUTUBE_COOKIES"])
    temp_cookie_file.close()
    cookie_file_path = temp_cookie_file.name
    st.sidebar.success("✅ YouTube Vault Active")

# --- 3. DOWNLOAD LOGIC ---
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("Paste Link Here:", placeholder="https://...")

if url:
    try:
        is_youtube = "youtube" in url or "youtu.be" in url
        
        ydl_opts = {
            # THE FIX: This format string is much more flexible. 
            # It tries for 1080p MP4 first, but if that's "not available", 
            # it grabs the best single-file (video+audio together) version.
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
            'noplaylist': True,
        }

        if is_youtube:
            if cookie_file_path:
                ydl_opts['cookiefile'] = cookie_file_path
            
            # Using specific "Android" client args which are currently more stable for cloud IPs
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['android', 'web'],
                }
            }
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            }

        with st.spinner("Bypassing restrictions and downloading..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Clear cache to reset any "Format Not Available" flags from YouTube
                ydl.cache.remove()
                
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Check for extension changes during the merge process
                if not os.path.exists(file_path):
                    base = os.path.splitext(file_path)[0]
                    for ext in ['.mp4', '.mkv', '.webm']:
                        if os.path.exists(base + ext):
                            file_path = base + ext
                            break

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label="💾 Download to Device",
                    data=f,
                    file_name=os.path.basename(file_path)
                )
            st.success("Success!")
        else:
            st.error("File download failed. YouTube might be blocking this specific server.")

    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)

# --- 4. SIDEBAR CLEANUP ---
if st.sidebar.button("🗑️ Clear Cache"):
    shutil.rmtree("downloads")
    os.makedirs("downloads")
    st.sidebar.write("Cache Cleared.")
