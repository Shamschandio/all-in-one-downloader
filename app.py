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
url = st.text_input("ENTER VIDEO LINK:", placeholder="Paste link here...")

if url:
    try:
        cookie_path = None
        if "YOUTUBE_COOKIES" in st.secrets:
            t = tempfile.NamedTemporaryFile(delete=False, mode='w')
            t.write(st.secrets["YOUTUBE_COOKIES"])
            t.close()
            cookie_path = t.name

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'cookiefile': cookie_path,
            'nocheckcertificate': True,
            'quiet': True,
            
            # THE 403 NUCLEAR BYPASS (DEC 2025)
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'mweb'],
                    # This helps bypass the initial 403 handshake
                    'skip': ['web'],
                }
            },
            # Masking the request to look like a direct Google search referral
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.google.com/',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        }

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        with st.spinner("CRACKING ENCRYPTION..."):
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
            st.success("BYPASS SUCCESSFUL")

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
        st.info("💡 403 FIX: Your cookies might be 'stale'. Try exporting them again from an Incognito tab where you are logged into YouTube.")
    finally:
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)

if st.sidebar.button("🗑️ RESET CACHE"):
    shutil.rmtree("downloads")
    os.makedirs("downloads")
    st.sidebar.write("System Reset.")
