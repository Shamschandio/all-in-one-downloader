import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Social Experiment Downloader", page_icon="🎬")
st.title("🎬 Social Experiment Downloader")
st.markdown("Download from **YouTube, TikTok, or Instagram**.")

# --- 2. LOAD COOKIES FROM SECRETS ---
cookie_file_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    temp_cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w')
    temp_cookie_file.write(st.secrets["YOUTUBE_COOKIES"])
    temp_cookie_file.close()
    cookie_file_path = temp_cookie_file.name
    st.sidebar.success("✅ YouTube Vault Active")
else:
    st.sidebar.warning("⚠️ No Cookies in Vault.")

# --- 3. SIDEBAR TOOLS ---
with st.sidebar:
    st.header("Admin Tools")
    if st.button("🗑️ Clear Server Cache"):
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
            os.makedirs("downloads")
            st.success("Cache cleared!")

# --- 4. MAIN DOWNLOADER LOGIC ---
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("Paste Link Here:", placeholder="YouTube, Shorts, TikTok, or Instagram...")

if url:
    try:
        is_youtube = "youtube.com" in url or "youtu.be" in url
        
        ydl_opts = {
            # THE FIX: 'best' is the most compatible setting. 
            # It avoids the 'Format not available' error by picking whatever works.
            'format': 'bestvideo+bestaudio/best',
            'check_formats': True,
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'nocheckcertificate': True,
        }

        if is_youtube:
            if cookie_file_path:
                ydl_opts['cookiefile'] = cookie_file_path
            
            # Additional bypasses for YouTube's recent security updates
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['ios', 'mweb', 'web'],
                    'player_js_version': 'actual'
                }
            }
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            }

        with st.spinner("Finding best available quality..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Handling the case where merging changes the extension
                if not os.path.exists(file_path):
                    base = os.path.splitext(file_path)[0]
                    for ext in ['.mp4', '.mkv', '.webm', '.3gp']:
                        if os.path.exists(base + ext):
                            file_path = base + ext
                            break

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label="💾 Save Video to Device",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4"
                )
            st.balloons()
            
    except Exception as e:
        st.error(f"Download Error: {e}")
    finally:
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)
