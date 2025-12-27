import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# 1. App Configuration
st.set_page_config(page_title="Social Experiment Downloader", page_icon="🎬")
st.title("🎬 Social Experiment Downloader")

# --- 2. LOAD COOKIES FROM SECRETS VAULT ---
cookie_file_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    # Use 'w' mode to write the secret string into a real file for yt-dlp to read
    temp_cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w')
    temp_cookie_file.write(st.secrets["YOUTUBE_COOKIES"])
    temp_cookie_file.close()
    cookie_file_path = temp_cookie_file.name
    st.sidebar.success("✅ Cookies loaded from Vault")
else:
    st.sidebar.error("❌ Cookies not found in Secrets!")

# --- 3. SIDEBAR TOOLS (ADMIN) ---
with st.sidebar:
    st.header("Admin Tools")
    if st.button("🗑️ Clear Server Cache"):
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
            os.makedirs("downloads")
            st.success("Cache cleared!")
        else:
            st.info("Cache is already empty.")

# --- 4. DOWNLOADER LOGIC ---
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("Enter Video URL (YouTube, Shorts, etc):", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # These options are tuned for 2025 YouTube changes
        ydl_opts = {
            # 'format_sort' is better than 'format'. It tells yt-dlp to find the 
            # best quality automatically without crashing if a specific codec is missing.
            'format_sort': [
                'res:1080',      # Prefer 1080p (stable for cloud)
                'ext:mp4:m4a',   # Prefer MP4 container
                'codec:h264:aac' # Prefer highly compatible codecs
            ],
            'check_formats': True,          # Skips DRM-protected formats automatically
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'cookiefile': cookie_file_path,
            'quiet': True,
            'nocheckcertificate': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'mweb', 'web'],
                    'player_js_version': 'actual'
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            },
        }

        with st.spinner("Analyzing and downloading..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Handling cases where the extension might change during merging
                if not os.path.exists(file_path):
                    base = os.path.splitext(file_path)[0]
                    for ext in ['.mp4', '.mkv', '.webm']:
                        if os.path.exists(base + ext):
                            file_path = base + ext
                            break

        with open(file_path, "rb") as f:
            st.download_button(
                label="💾 Save Video to Device",
                data=f,
                file_name=os.path.basename(file_path),
                mime="video/mp4"
            )
            st.balloons()
            
    except Exception as e:
        st.error(f"Download Error: {e}")
        st.info("Tip: If it still fails, try a different video. Some 'Premium' or 'Music' content is strictly locked by YouTube.")
    finally:
        # Cleanup the temporary cookie file
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)
