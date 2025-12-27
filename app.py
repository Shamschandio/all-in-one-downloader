import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. APP CONFIG ---
st.set_page_config(page_title="Universal Downloader", page_icon="🚀")
st.title("🚀 Universal Video Downloader")
st.info("Works for YouTube, TikTok, and Instagram.")

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

url = st.text_input("Paste your link here:")

if url:
    try:
        is_youtube = "youtube" in url or "youtu.be" in url
        
        ydl_opts = {
            # THE CRITICAL FIX: 
            # This format string tries 1080p/720p first, 
            # but 'b' at the end means "just give me the best single file if all else fails"
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
        }

        if is_youtube:
            if cookie_file_path:
                ydl_opts['cookiefile'] = cookie_file_path
            
            # Use Mobile Safari headers to bypass "Requested Format" blocks
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
            }
            ydl_opts['extractor_args'] = {'youtube': {'player_client': ['mweb', 'ios']}}

        with st.spinner("Downloading... please wait."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Clear cache to prevent old errors from sticking
                ydl.cache.remove()
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Verify file extension (sometimes it ends up as .mkv or .webm)
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
            st.success("Download Ready!")
        else:
            st.error("Could not find the downloaded file.")

    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)

# --- 4. CLEANUP BUTTON ---
if st.sidebar.button("Clear Server Cache"):
    shutil.rmtree("downloads")
    os.makedirs("downloads")
    st.sidebar.write("Cache Cleared.")
