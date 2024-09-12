import streamlit as st
from Firebase.cred import initialize_firebase
from Firebase.authenticate import create_user  # Use Firebase function for creating new users
from Firebase.db_interaction import NGO_Database  # Use NGO_Database to interact with Firestore
import base64
import time
# from Image_Detection.image_to_text import *

def ngo_registration(db):
    st.header("NGO Registration")
    st.write("Fill out the form below to register your NGO.")

    # Input fields for NGO registration
    ngo_name = st.text_input("NGO Name", max_chars=100)
    description = st.text_area("NGO Description", max_chars=500)
    email = st.text_input("Contact Email")
    password = st.text_input("Create Password", type="password")
    needs = st.text_area("List of Needs (e.g., food, clothes, books)", help="Separate items by commas")
    image_logo = st.file_uploader("Upload NGO Logo", type=["jpg", "jpeg", "png"])
    phone = st.text_input("Contact Phone Number", max_chars=10)

    if st.button("Register"):
        if ngo_name and description and email and password and needs:
            # Initialize Firebase
            # db = initialize_firebase()
            ngo_db = NGO_Database(db)

            # Create a new Firebase user
            id_token = create_user(email, password)
            time.sleep(1)
            if id_token:
                # Prepare data
                needs_list = [item.strip().lower() for item in needs.split(',')]
                ngo_data = {
                    "Name": ngo_name,
                    "Description": description,
                    "email": email,
                    "needs": needs,
                    "Phone": phone,
                }

                # Register the NGO in Firestore
                image_bytes = image_logo.read()
                encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                ngo_db.add_NGO(id_token, ngo_name, "General", encoded_image, description, phone,needs_list,email)
                st.success("NGO Registered Successfully!")
            else:
                st.error("Failed to register. Please try again.")
        else:
            st.error("Please fill in all fields to register.")

if __name__ == "__main__":
    ngo_registration()
