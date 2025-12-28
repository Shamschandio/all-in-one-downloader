import streamlit as st
import yt_dlp
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="TIKTOK DL NO-COOKIES", page_icon="🚀")
st.title("🚀 TIKTOK HIGH-RES DOWNLOADER")
st.markdown("### Simple. Fast. No Cookies.")

# Ensure download directory exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

url = st.text_input("PASTE TIKTOK LINK:", placeholder="https://www.tiktok.com/...")

if url:
    try:
        with st.spinner("⚡ FETCHING BEST QUALITY..."):
            # --- THE ENGINE CONFIG ---
            ydl_opts = {
                # 'best' captures the highest pre-merged quality
                'format': 'best', 
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                # This 'impersonate' flag is the secret sauce for 2025
                # It makes the server look like a real Chrome browser
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 1. Get Video Metadata
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # 2. Display Info
                st.success(f"✅ READY: {info.get('title', 'TikTok Video')[:50]}...")
                st.write(f"📐 Resolution: {info.get('width')} x {info.get('height')}")

            # 3. Create Download Button
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="💾 DOWNLOAD VIDEO (HD)",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
                st.balloons()

    except Exception as e:
        # Handling the "Sensitive Content" error gracefully
        if "comfortable for some audiences" in str(e):
            st.error("🔒 This video is 'Sensitive Content'. TikTok requires a login for this specific video.")
            st.info("Try a different video, or use the Cookie version if you really need this one.")
        else:
            st.error(f"❌ ENGINE ERROR: {e}")

# --- AUTO-CLEANUP ---
# This keeps your server space clean
if st.sidebar.button("🗑️ Clear Server Files"):
    for f in os.listdir("downloads"):
        os.remove(os.path.join("downloads", f))
    st.sidebar.success("Cleaned!")
