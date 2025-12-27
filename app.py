import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. RESTORE ORIGINAL BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K DOWNLOADER")
st.markdown("---")

# --- 2. LOAD COOKIES FROM VAULT ---
cookie_file_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    temp_cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w')
    temp_cookie_file.write(st.secrets["YOUTUBE_COOKIES"])
    temp_cookie_file.close()
    cookie_file_path = temp_cookie_file.name
    st.sidebar.success("✅ 4K Access Token Active")

# --- 3. DOWNLOAD ENGINE ---
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("ENTER VIDEO LINK (YouTube, TikTok, Instagram):", placeholder="Paste link here...")

if url:
    try:
        is_youtube = "youtube" in url or "youtu.be" in url
        
        ydl_opts = {
            # FIX: We use Sort instead of a strict Format ID.
            # This stops the 'Requested format not available' error.
            'format_sort': ['res:2160', 'res:1080', 'ext:mp4:m4a'], 
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
        }

        if is_youtube:
            if cookie_file_path:
                ydl_opts['cookiefile'] = cookie_file_path
            
            # Using the 'Android' and 'iOS' client bypasses for 2025 security
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['android', 'ios', 'mweb'],
                }
            }
            # Mask the server IP as a mobile browser
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
            }

        with st.spinner("PROBING 4K SERVERS..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Clear session cache to bypass temporary IP bans
                ydl.cache.remove()
                
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Check if the file merged into a different extension (mkv/webm)
                if not os.path.exists(file_path):
                    base = os.path.splitext(file_path)[0]
                    for ext in ['.mp4', '.mkv', '.webm']:
                        if os.path.exists(base + ext):
                            file_path = base + ext
                            break

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label="💾 SAVE TO DEVICE",
                    data=f,
                    file_name=os.path.basename(file_path)
                )
            st.balloons()
        else:
            st.error("Format Conflict: YouTube is blocking 4K for this specific IP. Trying fallback...")

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
    finally:
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)

# --- 4. ADMIN PANEL ---
if st.sidebar.button("🗑️ RESET CACHE"):
    shutil.rmtree("downloads")
    os.makedirs("downloads")
    st.sidebar.write("System Reset.")
