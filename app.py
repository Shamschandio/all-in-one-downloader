import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# 1. App Configuration & Title
st.set_page_config(page_title="Social Experiment Downloader", page_icon="🎬")
st.title("🎬 Social Experiment Downloader")

# --- 2. LOAD COOKIES FROM SECRETS VAULT ---
cookie_file_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    # Create a temporary file to act as the cookies.txt
    # delete=False is important so the file stays until we manually remove it
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

url = st.text_input("Enter Video URL:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # These options are specifically tuned to bypass 403 Forbidden errors
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
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
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            },
        }

        with st.spinner("Bypassing security and downloading..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Double check for the merged mp4 file
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
        st.info("Tip: If you see a 403 error, try rebooting the app via the 'Manage App' menu.")
    finally:
        # Cleanup the temporary cookie file to keep the server secure
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)
