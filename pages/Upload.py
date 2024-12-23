import streamlit as st
# display title
st.title(f"Upload a sqlite file!")

st.text("upload your sqlite file")
uploaded_sqlite_file = st.file_uploader("Choose a file")

if uploaded_sqlite_file is not None:
    # Save the uploaded file to the current directory
    with open(uploaded_sqlite_file.name, "wb") as f:
        f.write(uploaded_sqlite_file.getbuffer())

    st.text("File uploaded")