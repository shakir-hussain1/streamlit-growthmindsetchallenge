import streamlit as st 
import pandas as pd 
import os 
from io import BytesIO 

st.set_page_config(page_title="Data Sweeper", layout='wide') 

#Styling
st.markdown(
    """
<style>
.stApp{
    background-color: black;
    color:white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#Title and Description 
st.title("Datasweeper Sterling Integrator by Shakir Hussain") 
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization creating the project for quarter 3!") 

#File uploader 
uploaded_files=st.file_uploader("Upload your files (accepts CSV or excel):", type=["csv","xlsx"], accept_multiple_files=(True))
if uploaded_files: 
    for file in uploaded_files:
        file_ext= os.path.splitext(file.name)[-1].lower() 

        if file_ext== ".csv":
            df=pd.read_csv(file)
        elif file_ext== "xlsx":
            df=pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}") 
            continue 

        #File details
        st.write("Preview tha head of the Dataframe")
        st.dataframe(df.head()) 
        
        #Data cleaning options
        st.subheader("Data cleaning options")
        if st.checkbox(f"Clean data for {file.name}"): 
            col1,col2=st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed...")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols=df.select_dtypes(include=['number']).columns
                    df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled...")

        st.subheader("Select column to keep")
        columns=st.multiselect("Choose columns for {file.name}", df.columns, default=df.columns)
        df=df[columns]

        #Data visualization
        st.subheader("Data visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #Conversion options
        st.subheader("Conversion options")
        conversion_type=st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer=BytesIO()
            if conversion_type=="CSV":
                df.to.csv(buffer, index=False)
                file_name=file.name.replace(file_ext, ".csv")
                mime_type="text/csv"

            elif conversion_type=="Excel":
                df.to.excel(buffer, index=False)
                file_name=file.name.replace(file_ext, ".excel")
                mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed successfully...")