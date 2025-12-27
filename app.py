import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

# --- 1. ORIGINAL BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K DOWNLOADER")
st.markdown("---")

# --- 2. COOKIE HANDLER ---
cookie_file_path = None
if "YOUTUBE_COOKIES" in st.secrets:
    temp_cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w')
    temp_cookie_file.write(st.secrets["YOUTUBE_COOKIES"])
    temp_cookie_file.close()
    cookie_file_path = temp_cookie_file.name
    st.sidebar.success("✅ YouTube Access Active")

# --- 3. DOWNLOAD ENGINE ---
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("ENTER LINK (YT, TT, IG):", placeholder="Paste link here...")

if url:
    try:
        # Determine platform to avoid "Cross-Talk"
        is_youtube = "youtube" in url or "youtu.be" in url
        is_tiktok = "tiktok.com" in url
        is_insta = "instagram.com" in url

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
        }

        # PLATFORM SPECIFIC RULES
        if is_youtube:
            if cookie_file_path:
                ydl_opts['cookiefile'] = cookie_file_path
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
            }
        
        elif is_tiktok:
            # TikTok hates cookies and specific server headers
            ydl_opts['http_headers'] = {
                'User-Agent': 'com.zhiliaoapp.musically/2022405010 (Linux; U; Android 12; en_US; MP1605; Build/LMY48T; Cronet/TTNetVersion:5f74f74d 2022-05-01 QuicVersion:47535c59 2022-05-01)',
                'Accept': '*/*',
            }
        
        elif is_insta:
            # Instagram requires a basic mobile header
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36 Instagram 128.0.0.26.128 Android',
            }

        with st.spinner("COMMUNICATING WITH SERVERS..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove() 
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Check for merged extension
                if not os.path.exists(file_path):
                    base = os.path.splitext(file_path)[0]
                    for ext in ['.mp4', '.mkv', '.webm']:
                        if os.path.exists(base + ext):
                            file_path = base + ext
                            break

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(label="💾 SAVE TO DEVICE", data=f, file_name=os.path.basename(file_path))
            st.balloons()

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
    finally:
        if cookie_file_path and os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)

# --- 4. ADMIN ---
if st.sidebar.button("🗑️ RESET CACHE"):
    shutil.rmtree("downloads")
    os.makedirs("downloads")
    st.sidebar.write("System Reset.")
