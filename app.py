import streamlit as st
from pytubefix import YouTube
import os

# --- BRANDING ---
st.title("🎬 SOCIAL EXPERIMENT 4K")

url = st.text_input("ENTER VIDEO LINK:")

if url:
    try:
        # We define a specific folder for the 'Passport' to stay safe
        cache_dir = os.path.join(os.getcwd(), ".pytubefix_cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        with st.spinner("CHECKING AUTHORIZATION..."):
            # We point the cache to our local folder
            yt = YouTube(
                url, 
                use_oauth=True, 
                allow_oauth_cache=True,
                cache_dir=cache_dir 
            )
            
            # This line forces the app to check if we are logged in
            st.write(f"✅ CONNECTION ESTABLISHED: {yt.title}")
            
            # Grab the best MP4
            video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            
            if video:
                # Show file size so we know it's working
                st.info(f"File Size: {round(video.filesize_mb, 2)} MB")
                
                # Download
                path = video.download(output_path="downloads")
                
                with open(path, "rb") as f:
                    st.download_button("💾 DOWNLOAD NOW", f, file_name=os.path.basename(path))
                st.balloons()

    except Exception as e:
        st.error(f"ENGINE STATUS: {e}")
        st.info("💡 If you see a code in the logs, please enter it at google.com/device")
