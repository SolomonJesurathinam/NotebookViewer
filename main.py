import streamlit as st
from nbconvert.nbconvertapp import main as nbmain
import pdfkit
import os
from pathlib import Path
from streamlit_javascript import st_javascript
from streamlit_lottie import st_lottie
import json
import shutil

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

st.set_page_config(page_title="NB to PDF and HTML Converter")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

def clear_storage_if_needed(storage_dir, threshold=0.9):
    # Get disk usage statistics
    total, used, free = shutil.disk_usage(storage_dir)

    # Calculate the percentage of space used
    percent_used = used / total

    if(percent_used > 8.5):
        st.write(percent_used)

    # If used space exceeds the threshold, delete files
    if percent_used > threshold:
        for file in Path(storage_dir).iterdir():
            try:
                if file.is_file():
                    os.remove(file)
                    print(f"Deleted {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")

clear_storage_if_needed(current_dir /"files/")

def convert_notebook_to_html(notebook_path):
    nbmain(['--to', 'html', '--template', 'classic', notebook_path])


# Load your Lottie animation file
lottiepath = "loading.json"
with open(lottiepath, "r") as file:
    lottie_animation = json.load(file)

st.title("Jupyter NB to PDF and HTML Converter")

uploaded_file = st.file_uploader("Upload a Jupyter Notebook", type="ipynb")

if uploaded_file is not None:
    file_name = uploaded_file.name
    notebook_path = "files/" + file_name
    html_path = "files/" + file_name.replace(".ipynb", ".html")
    pdf_name = "files/" + file_name.replace(".ipynb", ".pdf")

    # Save the uploaded notebook temporarily
    with open(notebook_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    progress_bar = st.progress(0)
    status_message = st.empty()

    # Display Lottie animation during conversion
    lottie_container = st.empty()
    with lottie_container:
        st_lottie(lottie_animation, height=300, key="loading")

    if not os.path.exists(html_path) or not os.path.exists(pdf_name):
        if not os.path.exists(html_path):
            # Convert Notebook to HTML
            status_message.text("Converting notebook to HTML...")
            progress_bar.progress(25)
            convert_notebook_to_html(notebook_path)

        if not os.path.exists(pdf_name):
            # Convert HTML to PDF
            status_message.text("Converting HTML to PDF...")
            progress_bar.progress(50)
            try:
                pdfkit.from_file(html_path, pdf_name, options={"enable-local-file-access": ""}, verbose=True)
            except OSError as e:
                if 'Done' not in str(e):
                    st.error("Error while converting, please try another file or reload and try again")

    # Display HTML File and offer PDF for download
    progress_bar.progress(75)
    if os.path.exists(html_path) and os.path.exists(pdf_name):
        # Hide the Lottie animation
        lottie_container.empty()

        ui_width = st_javascript("window.innerWidth")
        with open(html_path, "r") as f:
            html_content = f.read()
            st.components.v1.html(html_content, width=ui_width, height=(ui_width * 4 / 3), scrolling=True)

        with open(pdf_name, "rb") as f:
            pdf_data = f.read()
            st.download_button(label="Download PDF", data=pdf_data, file_name=pdf_name, mime='application/octet-stream')
            status_message.text("Conversion complete! PDF is ready to download.")
        progress_bar.progress(100)

    # os.remove(file_name)
    # os.remove(html_path)
    # os.remove(pdf_name)
