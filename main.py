import streamlit as st
from nbconvert.nbconvertapp import main as nbmain
import pdfkit
import os
import base64
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

st.set_page_config(page_title="NB to Pdf Converter")

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html=True)

def convert_notebook_to_html(notebook_path):
    nbmain(['--to', 'html', '--template', 'classic', notebook_path])

st.title("Jupyter NB to Pdf Converter")

uploaded_file = st.file_uploader("Upload a Jupyter Notebook", type="ipynb")

if uploaded_file is not None:
    file_name = uploaded_file.name
    notebook_path = file_name
    html_path = file_name.replace(".ipynb", ".html")
    pdf_name = file_name.replace(".ipynb", ".pdf")

    # Save the uploaded notebook temporarily
    with open(notebook_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    progress_bar = st.progress(0)
    status_message = st.empty()

    # Convert Notebook to HTML
    status_message.text("Converting notebook to HTML...")
    progress_bar.progress(25)
    convert_notebook_to_html(notebook_path)

    # Convert HTML to PDF
    status_message.text("Converting HTML to PDF...")
    progress_bar.progress(50)
    try:
        pdfkit.from_file(html_path, pdf_name, options={"enable-local-file-access": ""},verbose=True)
    except OSError as e:
        if 'Done' not in str(e):
            st.error("Error while converting, please try another file")

    # Check if the PDF file was created
    status_message.text("Finalizing...")
    progress_bar.progress(75)
    if os.path.exists(pdf_name):
        with open(pdf_name, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            status_message.text("Preparing download...")
            progress_bar.progress(100)
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="100%" style="height:80vh;"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            PDFByte = f.read()
            status_message.text("Conversion complete! PDF is ready to download.")
            st.download_button(label="Download PDF", data=f, file_name=pdf_name, mime='application/pdf')