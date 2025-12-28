import streamlit as st
from pytubefix import YouTube
import os

# --- BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K")

url = st.text_input("PASTE YOUTUBE LINK:")

if url:
    try:
        with st.spinner("CONNECTING TO SOCIAL ENGINE..."):
            # We remove 'cookiefile' and 'use_oauth' to avoid the errors you saw
            # pytubefix will now use its default 'WEB' client which is currently stable
            yt = YouTube(url)
            
            # This line 'pings' YouTube to see if we are blocked
            st.subheader(f"📹 {yt.title}")
            
            # We grab the highest resolution MP4 available (720p/1080p)
            # This is the 'Progressive' stream which is easiest for Streamlit to handle
            video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            
            if video:
                st.info(f"Resolution: {video.resolution} | Size: {round(video.filesize_mb, 2)} MB")
                
                # Create downloads folder if it doesn't exist
                if not os.path.exists("downloads"):
                    os.makedirs("downloads")
                    
                path = video.download(output_path="downloads")
                
                with open(path, "rb") as f:
                    st.download_button(
                        label="💾 DOWNLOAD NOW",
                        data=f,
                        file_name=os.path.basename(path),
                        mime="video/mp4"
                    )
                st.balloons()
            else:
                st.error("No high-quality MP4 stream found for this video.")

    except Exception as e:
        # If this fails with a 403, we know it's a hard IP block
        st.error(f"ENGINE ERROR: {e}")
        if "403" in str(e):
            st.warning("⚠️ YouTube is blocking this server's IP. Please 'Reboot' the app in the Manage App menu to get a new IP.")
