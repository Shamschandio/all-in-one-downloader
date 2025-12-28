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
        ydl_opts = {
            # GUEST MODE: We stop using cookies to prevent the 'Invalid Cookies' error
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
            
            # THE 2025 GUEST BYPASS:
            # We use 'ios' and 'android' clients because they are the most 
            # likely to work WITHOUT a PO Token or Cookies.
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'],
                    'player_skip': ['web', 'mweb', 'android_embedded'], # Skip the clients that require tokens
                }
            },
            'http_headers': {
                'User-Agent': 'com.google.android.youtube/19.29.37 (Linux; U; Android 14; en_US; Pixel 8 Pro; Build/UQ1A.240205.004) [WR/1]',
            }
        }

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        with st.spinner("BYPASSING AS GUEST MOBILE..."):
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
            st.success("GUEST BYPASS SUCCESSFUL")

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
        st.info("💡 SECURITY ALERT: YouTube has blocked this Streamlit IP. Click 'Reboot' in the Manage App menu.")
