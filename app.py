import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K DOWNLOADER")
st.markdown("---")

# --- 2. ENGINE ---
url = st.text_input("PASTE LINK HERE:", placeholder="YouTube, TikTok, Instagram...")

if url:
    try:
        cookie_path = None
        if "YOUTUBE_COOKIES" in st.secrets:
            t = tempfile.NamedTemporaryFile(delete=False, mode='w')
            t.write(st.secrets["YOUTUBE_COOKIES"])
            t.close()
            cookie_path = t.name

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best', 
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'cookiefile': cookie_path,
            'nocheckcertificate': True,
            'quiet': True,
        }

        # TikTok Specific Bypasses
        if "tiktok.com" in url:
            ydl_opts['extractor_args'] = {'tiktok': {'web_client': True}}
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
                'Accept': '*/*',
            }

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        with st.spinner("SOCIAL EXPERIMENT IN PROGRESS..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove()
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
                st.download_button(label="💾 DOWNLOAD FILE", data=f, file_name=os.path.basename(file_path))
            st.balloons()
            st.success("DOWNLOAD READY")

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
    finally:
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)

if st.sidebar.button("🗑️ RESET SYSTEM"):
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
        os.makedirs("downloads")
    st.sidebar.write("Cache Cleared.")
