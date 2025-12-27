import streamlit as st
import yt_dlp
import os

# --- 1. BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K DOWNLOADER")

# --- 2. THE "OLD STYLE" ENGINE (With 2025 Fixes) ---
url = st.text_input("PASTE LINK HERE:", placeholder="YouTube, TikTok, Instagram...")

if url:
    try:
        ydl_opts = {
            # BACK TO BASICS: Try 4K, then 1080p, then whatever works.
            'format': 'bestvideo+bestaudio/best', 
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
        }

        # We MUST keep the cookies and headers, or the server IP will be 403'd instantly.
        if "YOUTUBE_COOKIES" in st.secrets:
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
                f.write(st.secrets["YOUTUBE_COOKIES"])
                ydl_opts['cookiefile'] = f.name

        with st.spinner("DOWNLOADING..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Handling merging issues (sometimes it saves as mkv)
                if not os.path.exists(file_path):
                    file_path = file_path.replace(".mp4", ".mkv")

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button("💾 DOWNLOAD FILE", f, file_name=os.path.basename(file_path))
            st.success("DONE!")

    except Exception as e:
        st.error(f"ERROR: {e}")
