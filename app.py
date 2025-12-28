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
            # Try 4K, but accept best available to prevent "Format Not Available"
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'cookiefile': cookie_path,
            'nocheckcertificate': True,
            'quiet': True,
            
            # 2025 SMART TV BYPASS:
            # Android TV and YouTube Music clients are currently bypassing the 403 blocks
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_embedded', 'tv', 'mweb'],
                    'player_skip': ['web', 'ios'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Android 14; TV; rv:120.0) Gecko/120.0 Firefox/120.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': 'https://www.youtube.com/tv',
            }
        }

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        with st.spinner("INITIATING SMART TV BYPASS..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove() # Important to clear previous 403 flags
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Check for merged file extension variations
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
            st.success("ACCESS GRANTED")

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
        st.info("💡 IP BLOCK: If you still see 403, YouTube has banned this Streamlit IP. Please click 'Reboot' in the sidebar menu.")
    finally:
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)

if st.sidebar.button("🗑️ RESET CACHE"):
    shutil.rmtree("downloads")
    os.makedirs("downloads")
    st.sidebar.write("System Reset.")
