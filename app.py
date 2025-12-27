import streamlit as st
import yt_dlp
import os
import tempfile  # <--- Added missing import to fix your error
import shutil

# --- 1. BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K DOWNLOADER")
st.markdown("---")

# --- 2. THE ENGINE ---
url = st.text_input("PASTE LINK HERE:", placeholder="YouTube, TikTok, or Instagram...")

if url:
    try:
        # Create a temporary file for cookies from Streamlit Secrets
        cookie_path = None
        if "YOUTUBE_COOKIES" in st.secrets:
            # delete=False is needed so the file stays alive for yt-dlp to read it
            t = tempfile.NamedTemporaryFile(delete=False, mode='w')
            t.write(st.secrets["YOUTUBE_COOKIES"])
            t.close()
            cookie_path = t.name

        # This configuration is the "Private Style" logic you preferred
        ydl_opts = {
            # Try to get 4K/1080p, but fall back to the best single file if hidden
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'cookiefile': cookie_path,
            'nocheckcertificate': True,
            'quiet': True,
        }

        # Make sure the download folder exists
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        with st.spinner("SOCIAL EXPERIMENT IN PROGRESS..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Clear yt-dlp internal cache to reset IP-based blocks
                ydl.cache.remove()
                
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Check if the file merged into a different format (like .mkv)
                if not os.path.exists(file_path):
                    base = os.path.splitext(file_path)[0]
                    for ext in ['.mp4', '.mkv', '.webm']:
                        if os.path.exists(base + ext):
                            file_path = base + ext
                            break

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label="💾 DOWNLOAD 4K FILE", 
                    data=f, 
                    file_name=os.path.basename(file_path)
                )
            st.balloons()
            st.success("DOWNLOAD READY")

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
        st.info("💡 TIP: If you see 'Format not available', try a fresh cookie export.")
    finally:
        # Cleanup: Remove the temporary cookie file for security
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)

# --- 3. ADMIN TOOLS ---
if st.sidebar.button("🗑️ RESET SYSTEM"):
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
        os.makedirs("downloads")
    st.sidebar.write("Cache Cleared.")
