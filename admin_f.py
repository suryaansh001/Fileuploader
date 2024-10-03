import streamlit as st
import pymysql
import os

# MySQL connection details from Streamlit secrets
db_config = {
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": st.secrets["DB_NAME"],
    "host": st.secrets["DB_HOST"],
    "port": int(st.secrets["DB_PORT"]),
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASSWORD"],
}

# Function to fetch submissions from the database
def fetch_submissions():
    submissions = []
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            fetch_query = "SELECT roll_number, name, file_path FROM submissions"
            cursor.execute(fetch_query)
            submissions = cursor.fetchall()
            # Log the fetched submissions for debugging
            st.write(f"Fetched submissions: {submissions}")
    except Exception as e:
        st.error("An error occurred while fetching submissions.")
        st.write(f"Error details: {e}")  # For debugging purposes
    finally:
        if 'connection' in locals():
            connection.close()
    return submissions

# Function to handle file download
def download_file(pdf_file_path, roll_number):
    # Log the file path for debugging
    st.write(f"Attempting to download file from path: {pdf_file_path}")
    
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, "rb") as f:
            pdf_data = f.read()
            st.download_button(
                label="Download File",
                data=pdf_data,
                file_name=f"{roll_number}_submission.pdf",
                mime="application/pdf"
            )
    else:
        st.error(f"The file for Roll Number {roll_number} does not exist.")
        st.write(f"Expected file path: {pdf_file_path}")

# Streamlit app
def main():
    st.title("JOC @ JKLU")
    
    menu = st.sidebar.selectbox("Select Action", ["View Uploaded Files"])
    
    if menu == "View Uploaded Files":
        st.header("Uploaded Files")
        
        submissions = fetch_submissions()
        
        if submissions:
            for submission in submissions:
                st.write(f"**Roll Number:** {submission['roll_number']}")
                st.write(f"**Name:** {submission['name']}")
                
                # Display download button
                pdf_file_path = submission['file_path']
                download_file(pdf_file_path, submission['roll_number'])
                
                st.write("---")  # Separator between submissions
        else:
            st.write("No submissions found.")

if __name__ == "__main__":
    main()

