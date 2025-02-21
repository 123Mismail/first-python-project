#import modules 
import streamlit as st
import pandas as pd
import os 
from io import BytesIO

st.set_page_config(page_title="🎈 Data sweeper", layout="centered")
st.title("(❁´◡`❁) Data Cleaner")
st.write("Here you can change your files into xls from csv and csv to xls and also clean up your data.")

uploaded_files = st.file_uploader(
    "Upload your files here (CSV or XLSX):", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
        
        # Displaying file information
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Showing some rows of the uploaded data
        st.write("**Preview of the data:**")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("Clean your data with the options below:")

        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicate data from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled")

        # Choosing columns 
        st.subheader("Select Columns to Convert ")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Converting the file now
        st.subheader("Convert your files")
        conversion_type = st.radio(f"Convert {file.name} to : ", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            else:
                st.error("Unsupported conversion type")
                continue
            
            buffer.seek(0)
            
            # Download button 
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
    
    st.success("🎉 All files processed")