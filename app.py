import streamlit as st
import requests

# --- BRANDING ---
st.set_page_config(page_title="SOCIAL EXPERIMENT 4K", page_icon="🎬")
st.title("🎬 SOCIAL EXPERIMENT 4K")
st.markdown("### RESTORED BYPASS MODE")

url = st.text_input("PASTE LINK (YouTube, TikTok, etc):")

if url:
    try:
        with st.spinner("COMMUNICATING WITH BYPASS SERVER..."):
            # We use the Cobalt API (a public reliable bypass)
            api_url = "https://api.cobalt.tools/api/json"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Requesting 1080p/4k quality
            payload = {
                "url": url,
                "videoQuality": "1080", # You can try "1440" or "2160" for 4K
                "filenameStyle": "pretty"
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            data = response.json()
            
            if data.get("status") == "stream":
                download_link = data.get("url")
                st.video(download_link) # Preview
                st.markdown(f'[💾 CLICK TO DOWNLOAD VIDEO]({download_link})')
                st.balloons()
            elif data.get("status") == "error":
                st.error(f"BYPASS ERROR: {data.get('text')}")
            else:
                st.error("Unexpected response from bypass server.")

    except Exception as e:
        st.error(f"SYSTEM ERROR: {e}")

st.info("NOTE: This method uses an external bypass engine to skip YouTube's 403 blocks.")
