import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# App configuration
st.set_page_config(page_title="Social Experiment Downloader", page_icon="🎬")
st.title("🎬 Social Experiment Downloader")

# --- STEP 1: LOAD COOKIES FROM SECRETS ---
cookie_file_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    # Create a temporary file to act as the cookies.txt
    temp_cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w')
    temp_cookie_file.write(st.secrets["YOUTUBE_COOKIES"])
    temp_cookie_file.close()
    cookie_file_path = temp_cookie_file.name
    st.sidebar.success("✅ Cookies loaded from Vault")
else:
    st.sidebar.error("❌ Cookies not found in Secrets!")

# --- STEP 2: SIDEBAR TOOLS (CACHE CLEANER) ---
with st.sidebar:
    st.header("Admin Tools")
    if st.button("🗑️ Clear Server Cache"):
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
            os.makedirs("downloads")
            st.success("Cache cleared!")
        else:
            st.info("Cache is already empty.")

# --- STEP 3: DOWNLOADER LOGIC ---
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("Enter Video URL:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'cookiefile': cookie_file_path,  # Uses the vault data
            'quiet': True,
            'nocheckcertificate': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
        }

        with st.spinner("Processing... this takes a moment for 4K."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                # Check for merged file extension
                if not os.path.exists(file_path):
                    file_path = os.path.splitext(file_path)[0] + ".mp4"

        with open(file_path, "rb") as f:
            st.download_button(
                label="💾 Save Video to Device",
                data=f,
                file_name=os.path.basename(file_path),
                mime="video/mp4"
            )
            
    except Exception as e:
        st.error(f"Download Error: {e}")
    finally:
        # Securely remove the temporary cookie file after use
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)
