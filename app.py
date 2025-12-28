import streamlit as st
from pytubefix import YouTube
import os

# --- BRANDING ---
st.title("🎬 SOCIAL EXPERIMENT 4K")

url = st.text_input("PASTE LINK:")

if url:
    try:
        # We check if cookies are in secrets
        cookie_content = st.secrets.get("YOUTUBE_COOKIES")
        
        cookie_path = None
        if cookie_content:
            # We save the cookies to a temporary file for the engine to read
            with open("cookies.txt", "w") as f:
                f.write(cookie_content)
            cookie_path = "cookies.txt"

        with st.spinner("INJECTING COOKIE PASSPORT..."):
            # Instead of OAuth, we use the cookie file
            yt = YouTube(
                url,
                use_oauth=False, # Disable the code/loading loop
                allow_oauth_cache=False,
                cookiefile=cookie_path if cookie_path else None
            )
            
            st.write(f"✅ ENGINE READY: {yt.title}")
            
            # Select the best available MP4 (720p/1080p)
            video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            
            if video:
                st.info(f"Size: {round(video.filesize_mb, 2)} MB")
                path = video.download(output_path="downloads")
                
                with open(path, "rb") as f:
                    st.download_button("💾 DOWNLOAD NOW", f, file_name=os.path.basename(path))
                st.balloons()

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
    finally:
        # Cleanup cookies for security
        if os.path.exists("cookies.txt"):
            os.remove("cookies.txt")
