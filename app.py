import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K DOWNLOADER")
st.markdown("---")

# --- 2. THE GUEST ENGINE ---
url = st.text_input("ENTER VIDEO LINK:", placeholder="Paste link here...")

if url:
    try:
        ydl_opts = {
            # Use 'best' to ensure we get something even if 4K is hidden
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
            
            # 2025 GUEST BYPASS: 
            # We use 'android_vr' and 'android_test'. 
            # These clients are currently the least restricted by PO-Tokens.
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_test', 'android_vr', 'ios'],
                    'player_skip': ['web', 'mweb', 'android'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            }
        }

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        with st.spinner("INITIATING GUEST BYPASS..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Force cache removal to drop the '403' flag from the server memory
                ydl.cache.remove()
                
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Check for merged file extensions
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
        st.info("💡 IP BLACKLIST: If 403 persists, the server IP is banned. Click 'Reboot' in the Manage App menu.")
