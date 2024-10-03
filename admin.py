import streamlit as st
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MySQL connection details from environment variables
db_config = {
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),  # Don't forget to add this line
}

# Function to fetch submissions from the database
def fetch_submissions():
    submissions = []
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            fetch_query = "SELECT roll_number, name, file_path FROM submissions"  # Use file_path instead of file_content
            cursor.execute(fetch_query)
            submissions = cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching submissions: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
    return submissions

# Streamlit app
def main():
    st.title("JOC @ JKLU")
    
    menu = st.sidebar.selectbox("Select Action", ["View Uploaded Files"],)
    
    
    if menu == "View Uploaded Files":
        st.header("Uploaded Files")
        
        submissions = fetch_submissions()
        
        if submissions:
            for submission in submissions:
                st.write(f"**Roll Number:** {submission['roll_number']}")
                st.write(f"**Name:** {submission['name']}")
                
                # Display download button
                pdf_file_path = submission['file_path']
                if st.button(f"Download PDF for {submission['roll_number']}"):
                    with open(pdf_file_path, "rb") as f:
                        pdf_data = f.read()
                        st.download_button(
                            label="Download File",
                            data=pdf_data,
                            file_name=f"{submission['roll_number']}_submission.pdf",
                            mime="application/pdf"
                        )
                
                st.write("---")  # Separator between submissions
        else:
            st.write("No submissions found.")

if __name__ == "__main__":
    main()

