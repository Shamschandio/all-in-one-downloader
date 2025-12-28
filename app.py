import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K DOWNLOADER")
st.markdown("---")

# --- 2. THE VR ENGINE ---
url = st.text_input("ENTER VIDEO LINK:", placeholder="Paste link here...")

if url:
    try:
        ydl_opts = {
            # VR clients often serve different formats, so we keep it flexible
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
            
            # THE VR BYPASS:
            # android_vr is currently the 'blind spot' in YouTube's PO Token enforcement
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_vr'],
                    'player_skip': ['web', 'mweb', 'ios', 'android', 'android_test'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Quest 3) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/31.0.0.14.106 SamsungBrowser/4.0 Chrome/119.0.6045.193 Mobile Safari/537.36',
            }
        }

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        with st.spinner("INITIATING VR-CLIENT BYPASS..."):
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
            st.success("VR BYPASS SUCCESSFUL")

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
        st.info("💡 IP LIMIT: If this fails, the IP is fully flagged. Rebooting is required.")
