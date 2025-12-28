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
            # THE FIX: This format string is 'Elastic'.
            # 1. It tries to merge the best mp4 video and m4a audio.
            # 2. If merging fails (no ffmpeg or hidden formats), it grabs the 'best' single file.
            # 3. If that fails, it grabs 'any' working stream.
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'cookiefile': cookie_path,
            'nocheckcertificate': True,
            'quiet': True,
            
            # Mobile clients are seeing more formats than Web clients right now
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'mweb'],
                }
            },
        }

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        with st.spinner("SEARCHING FOR BEST AVAILABLE QUALITY..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove()
                # Extract info first to see what formats YouTube is actually showing us
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
            st.success(f"SUCCESS: Downloaded as {info.get('format_note', 'Best Available')}")

    except Exception as e:
        # If even the elastic format fails, it's a hard block
        st.error(f"ENGINE ERROR: {e}")
    finally:
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)

if st.sidebar.button("🗑️ RESET CACHE"):
    shutil.rmtree("downloads")
    os.makedirs("downloads")
    st.sidebar.write("Cache Cleared.")
