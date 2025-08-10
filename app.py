import streamlit as st
import requests

# GitHub API URL for repo contents
GITHUB_API_URL = "https://api.github.com/repos/sravanik122/data/contents"

st.set_page_config(page_title="Telugu & English Recipes", page_icon="🍲", layout="wide")

# Sidebar
st.sidebar.title("🍲 Food Recipes")
st.sidebar.markdown("Search, view, and download your favorite recipes.")

# Language toggle
language = st.sidebar.radio("Select Language", ["English", "Telugu"])

# Search box
search_query = st.sidebar.text_input("🔍 Search for a recipe:")

# Fetch file list from GitHub
response = requests.get(GITHUB_API_URL)
if response.status_code != 200:
    st.error("❌ Failed to fetch data from GitHub.")
    st.stop()

files = response.json()

# Filter only .txt files
txt_files = [file for file in files if file['name'].endswith(".txt")]

# Filter based on language
if language == "English":
    txt_files = [file for file in txt_files if not file['name'].endswith("_te.txt")]
else:  # Telugu
    txt_files = [file for file in txt_files if file['name'].endswith("_te.txt")]

# Filter by search query
if search_query:
    txt_files = [file for file in txt_files if search_query.lower() in file['name'].lower()]

# Main content
st.title(f"📖 {language} Food Recipe Collection")

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
    st.warning(f"No {language} recipes found matching your search.")

