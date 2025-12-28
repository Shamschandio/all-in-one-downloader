import streamlit as st
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

# --- BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K")
st.markdown("### EMERGENCY BYPASS MODE (DEC 2025)")

url = st.text_input("ENTER VIDEO LINK:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        with st.spinner("INITIATING HANDSHAKE..."):
            # 'use_oauth=True' is the secret weapon for 2025. 
            # It will ask you to authorize once via a code, then never again.
            yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
            
            st.subheader(f"📹 {yt.title}")
            
            # Filtering for the highest resolution MP4
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            
            if video:
                out_file = video.download(output_path="downloads")
                
                with open(out_file, "rb") as f:
                    st.download_button(
                        label="💾 DOWNLOAD VIDEO",
                        data=f,
                        file_name=os.path.basename(out_file),
                        mime="video/mp4"
                    )
                st.balloons()
            else:
                st.error("No compatible MP4 streams found.")

    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
        st.info("💡 If this is your first time today, check the Streamlit logs for a 6-digit 'Device Code' to authorize the app.")
