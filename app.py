import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K DOWNLOADER")
st.markdown("---")

# --- 2. SECURE COOKIES ---
cookie_file_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    temp_cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w')
    temp_cookie_file.write(st.secrets["YOUTUBE_COOKIES"])
    temp_cookie_file.close()
    cookie_file_path = temp_cookie_file.name
    st.sidebar.success("✅ 4K Access Token Active")

# --- 3. DOWNLOAD ENGINE ---
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("ENTER VIDEO LINK:", placeholder="YouTube, TikTok, Instagram...")

if url:
    try:
        is_youtube = "youtube" in url or "youtu.be" in url
        
        ydl_opts = {
            # Try for 4K/1080p, but fallback to 'best' if YouTube hides them
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
            
            # Using web_embedded bypasses the need for Deno/JS Runtime
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['web_embedded', 'mweb', 'ios'],
                    'player_js_version': 'actual'
                }
            }
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.youtube.com/',
            }

        with st.spinner("PROBING SERVERS..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove() 
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Check for merged extension (.mkv or .webm)
                if not os.path.exists(file_path):
                    base = os.path.splitext(file_path)[0]
                    for ext in ['.mp4', '.mkv', '.webm']:
                        if os.path.exists(base + ext):
                            file_path = base + ext
                            break

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(label="💾 SAVE TO DEVICE", data=f, file_name=os.path.basename(file_path))
            st.balloons()

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
    finally:
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)

# --- 4. SYSTEM RESET ---
if st.sidebar.button("🗑️ RESET CACHE"):
    shutil.rmtree("downloads")
    os.makedirs("downloads")
    st.sidebar.write("System Reset.")
