import streamlit as st
import pymysql
import os
import io
import uuid
import base64
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# MySQL connection details from environment variables
db_config = {
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": st.secrets["general"]["DB_NAME"],
    "host": st.secrets["general"]["DB_HOST"],
    "port": int(st.secrets["general"]["DB_PORT"]),
    "user": st.secrets["general"]["DB_USER"],
    "password": st.secrets["general"]["DB_PASSWORD"],
}

# Function to fetch submissions from the database
def fetch_submissions():
    submissions = []
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            fetch_query = "SELECT roll_number, name, file_content FROM submissions"
            cursor.execute(fetch_query)
            submissions = cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching submissions: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
    return submissions

# Function to handle file viewing and downloading
def admin_file_viewer(file_content, roll_number, index):
    if file_content:
        # Convert the binary data to a file-like object
        pdf_file = io.BytesIO(file_content)

        # Encode PDF file in base64 for viewing
        pdf_base64 = base64.b64encode(pdf_file.getvalue()).decode('utf-8')
        pdf_url = f"data:application/pdf;base64,{pdf_base64}"

        # Unique key for the download button
        download_key = f"download_{roll_number}_{index}"

        # Download button
        st.download_button(
            label=f"Download {roll_number}'s Submission",
            data=pdf_file,
            file_name=f"{roll_number}_submission.pdf",
            mime="application/pdf",
            key=download_key  # Unique key
        )

        # Fullscreen viewing button
        st.markdown(
            f'<a href="{pdf_url}" target="_blank" rel="noopener noreferrer"><button>View {roll_number}\'s Submission in Fullscreen</button></a>',
            unsafe_allow_html=True
        )
        
    else:
        st.error(f"No file content available for Roll Number {roll_number}.")

# Main function for admin actions
def admin_main():
    st.title("Admin Panel - JOC @ JKLU")

    # Admin menu options
    menu = st.sidebar.selectbox("Select Action", ["View Uploaded Files"])

    if menu == "View Uploaded Files":
        st.header("Uploaded Files")

        # Fetch submissions from the database
        submissions = fetch_submissions()

        if submissions:
            # Display each submission details and allow PDF download/view
            for index, submission in enumerate(submissions):
                st.write(f"**Roll Number:** {submission['roll_number']}")
                st.write(f"**Name:** {submission['name']}")
                
                # Get the file content from the submission record
                file_content = submission['file_content']
                
                # Allow admin to view and download the file
                admin_file_viewer(file_content, submission['roll_number'], index)
                
                st.write("---")  # Separator between submissions
        else:
            st.write("No submissions found.")

# Execute admin_main() when the script runs
if __name__ == "__main__":
    admin_main()


