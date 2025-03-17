import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="GhostSweep", page_icon="🧊", layout="wide")

st.markdown(
    """
    <style>
        /* Dark Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #111, #222);
            color: #FFF;
            font-family: 'Poppins', sans-serif;
        }

        /* Glassmorphic Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Darken File Upload Box */
        .stFileUploader {
            background: #333 !important;
            color: #FFF !important;
            border: 2px solid #444 !important;
            border-radius: 10px;
            padding: 10px;
        }

        /* Title Styling */
        .stTitle {
            font-size: 2.8em;
            font-weight: 700;
            text-align: center;
            color: #FFFAFA;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        /* Section Headers */
        .stSubheader {
            font-size: 1.8em;
            font-weight: 600;
            color: #FFD700;
            margin-top: 20px;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #FF4500, #DC143C);
            color: white;
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #DC143C, #FF4500);
            transform: scale(1.05);
        }

        /* DataFrame Styling */
        .stDataFrame table {
            background-color: #222 !important;
            color: #FFF !important;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤍 GhostSweep")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

uploaded_files = st.file_uploader("Choose a file (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
            st.success("✅ CSV file loaded successfully!")
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
            st.success("✅ Excel file loaded successfully!")
        else:
            st.error(f"❌ File type not supported: {file_ext}")
            continue

        st.write(f"**📂 Filename:** {file.name}")
        st.write(f"**📏 File size:** {file.size/1024:.2f} KB")

        st.write("📊 **Preview the head of the Dataframe**")
        st.dataframe(df.head())

        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"✨ Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed successfully!")

            with col2:
                if st.button(f"🛠 Fill missing values from {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled successfully!")

        st.subheader("📌 Choose Specific Columns to Keep or Convert")
        columns = st.multiselect(f"📝 Select columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]           

        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        st.subheader("🔁 Conversion Options")
        conversion_type = st.radio(f"💾 Convert {file.name} to:", ["CSV", "Excel"], key=file.name) 
        if st.button(f"📂 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            st.download_button(label="📥 Download File", data=buffer.getvalue(), file_name=file_name, mime=mime_type)
            st.success(f"✅ {file.name} converted to {conversion_type} successfully!")





           




       