import streamlit as st
import pandas as pd
import os
import time
from io import BytesIO

# Streamlit Page Config
st.set_page_config(page_title="Muhammad Shahroz", layout="wide")

st.title("🚀 Simple Data Sweeper By Muhammad Shahroz")
st.write("Upload a file, clean the data, visualize insights, and download it!")

# File Upload
uploaded_file = st.file_uploader("Upload a file (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    # File Extension Check
    file_extension = os.path.splitext(uploaded_file.name)[-1].lower()

    # Read File
    if file_extension == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_extension == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error(f"Unsupported file type: {file_extension}")
        st.stop()

    # Session Storage
    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = df.copy()

    # File Info
    st.write(f"📄 **File Name:** {uploaded_file.name}")
    st.write(f"📏 **File Size:** {uploaded_file.size / 1024:.2f} KB")

    # Preview Data
    st.dataframe(st.session_state.cleaned_df)

    # Data Cleaning
    st.subheader("🛠️ Data Cleaning Options")

    # Remove Duplicates
    if st.button("Remove Duplicates"):
        before = len(st.session_state.cleaned_df)
        st.session_state.cleaned_df.drop_duplicates(inplace=True, ignore_index=True)
        after = len(st.session_state.cleaned_df)

        if before == after:
            st.warning("⚠️ No duplicates found!")
        else:
            st.success(f"✔️ Removed {before - after} duplicate rows!")
            time.sleep(2)
            st.rerun()

    # Column Selection
    selected_columns = st.multiselect("🎯 Select Columns", st.session_state.cleaned_df.columns, default=list(st.session_state.cleaned_df.columns))
    st.session_state.cleaned_df = st.session_state.cleaned_df[selected_columns]

    # Data Visualization
    st.subheader("📊 Data Visualization")
    if st.checkbox("Show Visualization"):
        numeric_df = st.session_state.cleaned_df.select_dtypes(include=['number'])

        if numeric_df.empty:
            st.info("No numeric columns available for visualization.")
        else:
            st.bar_chart(numeric_df)  # Simple Streamlit chart

    # File Conversion & Download
    st.subheader("🔄 Download File")
    conversion_type = st.radio("Convert file to:", ["CSV", "Excel"])

    if st.button("Download File"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            st.session_state.cleaned_df.to_csv(buffer, index=False)
            file_ext = ".csv"
            mime_type = "text/csv"
        else:
            st.session_state.cleaned_df.to_excel(buffer, index=False, engine='openpyxl')
            file_ext = ".xlsx"
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        buffer.seek(0)
        st.download_button(label=f"⬇️ Download {uploaded_file.name.replace(file_extension, file_ext)}", data=buffer, file_name=uploaded_file.name.replace(file_extension, file_ext), mime=mime_type)

else:
    st.info("📢 Upload a file to get started!")
