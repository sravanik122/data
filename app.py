import streamlit as st
import requests

st.title("📜 Telugu Recipe Dataset from GitHub")

# Correct GitHub API endpoint for your repo
api_url = "https://api.github.com/repos/Heena-Begum516/data/contents/"

response = requests.get(api_url)

if response.status_code == 200:
    try:
        items = response.json()
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and item.get("name", "").endswith(".txt"):
                    content = requests.get(item["download_url"]).text
                    st.subheader(item["name"].replace(".txt", ""))
                    st.text(content)
        else:
            st.error("Unexpected API response format:")
            st.write(items)
    except Exception as e:
        st.error(f"Error parsing API response: {e}")
else:
    st.error(f"Failed to fetch files (Status: {response.status_code})")
    st.write(response.text)
