import streamlit as st

# Function to read HTML content from a local file
def read_html_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

# Path to your HTML file
html_file_path = 'a.html'  # Replace with the path to your HTML file

# Read the HTML content from the file
html_content = read_html_file(html_file_path)

# Display the HTML content using st.components.v1.html
st.components.v1.html(html_content, width=None, height=1000, scrolling=True)
