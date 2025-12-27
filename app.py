import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K DOWNLOADER")
st.markdown("---")

# --- 2. SECURE COOKIE HANDLER ---
cookie_file_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    temp_cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w')
    temp_cookie_file.write(st.secrets["YOUTUBE_COOKIES"])
    temp_cookie_file.close()
    cookie_file_path = temp_cookie_file.name
    st.sidebar.success("✅ 4K Access Token Active")
else:
    st.sidebar.error("❌ No Cookies Found in Secrets!")

# --- 3. DOWNLOAD ENGINE ---
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("ENTER VIDEO LINK:", placeholder="YouTube, TikTok, Instagram...")

if url:
    try:
        is_youtube = "youtube" in url or "youtu.be" in url
        
        ydl_opts = {
            'format_sort': ['res:2160', 'res:1080', 'ext:mp4:m4a'], 
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
            'noplaylist': True,
        }

        if is_youtube:
            if cookie_file_path:
                ydl_opts['cookiefile'] = cookie_file_path
            
            # THE 403 BYPASS PACK:
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.youtube.com/',
            }
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['ios', 'mweb'],
                    'player_js_version': 'actual'
                }
            }

        with st.spinner("BYPASSING SECURITY..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove() # Clear internal blocks
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
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
        st.info("💡 TIP: If you see '403 Forbidden', try REBOOTING the app in the Manage App menu.")
    finally:
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)

# --- 4. SYSTEM RESET ---
if st.sidebar.button("🗑️ RESET CACHE"):
    shutil.rmtree("downloads")
    os.makedirs("downloads")
    st.sidebar.write("System Reset.")
