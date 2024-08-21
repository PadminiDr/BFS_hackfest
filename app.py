import streamlit as st

st.title("HEllo")

upload_files = st.file_uploader("Upload your transcripts", accept_multiple_files = True, type="zip")

for file in upload_files:
    bytes_data = file.read()
    st.write("write file: ", file.name, ".....")
    with open(f"files/{file.name}", "wb") as fr:
        fr.write(bytes_data)
    # st.write("filename: ", file.name)
    # st.write(bytes_data)