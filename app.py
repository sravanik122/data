import streamlit as st
import requests

# GitHub raw content link (replace with your dataset's raw URL)
GITHUB_API_URL = "https://api.github.com/repos/Heena-Begum516/data/contents"

st.set_page_config(page_title="Telugu Recipes", page_icon="🍲", layout="wide")

# Sidebar
st.sidebar.title("🍲 Telugu Food Recipes")
st.sidebar.markdown("Search, view, and download your favorite recipes.")

# Search box
search_query = st.sidebar.text_input("🔍 Search for a recipe:")

# Fetch file list from GitHub
response = requests.get(GITHUB_API_URL)
files = response.json()

# Filter .txt files only
txt_files = [file for file in files if file['name'].endswith(".txt")]

# Filter by search query
if search_query:
    txt_files = [file for file in txt_files if search_query.lower() in file['name'].lower()]

# Main content
st.title("📖 Telugu Food Recipe Collection")

if txt_files:
    for file in txt_files:
        file_name = file['name'].replace(".txt", "")
        file_url = file['download_url']

        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(file_name)
            recipe_text = requests.get(file_url).text
            st.text_area("Recipe Details", recipe_text, height=150)

        with col2:
            st.download_button(
                label="📥 Download",
                data=recipe_text,
                file_name=f"{file_name}.txt",
                mime="text/plain"
            )
        st.markdown("---")
else:
    st.warning("No recipes found matching your search.")
