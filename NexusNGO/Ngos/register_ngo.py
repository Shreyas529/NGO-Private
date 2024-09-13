import streamlit as st
from Firebase.cred import initialize_firebase
from Firebase.authenticate import create_user  # Use Firebase function for creating new users
from Firebase.db_interaction import NGO_Database  # Use NGO_Database to interact with Firestore
import time

def ngo_registration(db):
    # Apply custom CSS to match app.py style
    # st.markdown("""
    # <style>
    # body {
    #     background-color: #0F2027;
    #     background-image: linear-gradient(315deg, #0F2027 0%, #203A43 74%, #2C5364 100%);
    #     color: white;
    # }
    # h1, h2, h3, h4, h5, h6 {
    #     color: #60a5fa;
    #     text-align: center;
    # }
    # p {
    #     color: white;
    #     text-align: center;
    # }
    # .stButton > button {
    #     background-color: #FF4B4B ;
    #     color: white;
    #     border-radius: 30px;
    #     padding: 10px 24px;
    #     border: none;
    #     font-size: 16px;
    #     font-weight: 600;
    #     transition: all 0.3s ease;
    #     margin: 0 10px;
    #     width: 200px;
    # }
    # .stButton > button:hover {
    #     background-color: #FFFFFF ;
    #     color: #FF4B4B ;
    #     transform: scale(1.05);
    #     font-weight: bold;
    # }
    # .stTextInput, .stTextArea, .stFileUploader {
    #     background-color: #1e3c72 ;
    #     color: white;
    #     border: none;
    #     border-radius: 10px;
    # }
    # .stTextInput > input, .stTextArea > textarea, .stFileUploader > div {
    #     color: white ;
    # }
    # </style>
    # """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    body {
        background-color: #0F2027;
        background-image: linear-gradient(315deg, #0F2027 0%, #203A43 74%, #2C5364 100%);
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #60a5fa !important;
    }
    .stButton > button {
        background-color: #FF4B4B !important;  /* Update button color */
        color: white;
        border-radius: 30px;
        padding: 10px 24px;
        border: none;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 0 10px;
        width: 200px;
    }
    .stButton > button:hover {
        background-color: #FFFFFF !important;  /* Hover effect */
        color: #FF4B4B !important;
        transform: scale(1.05);
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # Page title and description
    st.markdown("<h2>NGO Registration</h2>", unsafe_allow_html=True)
    st.markdown("<p>Fill out the form below to register your NGO.</p>", unsafe_allow_html=True)

    # Input fields for NGO registration with consistent style
    ngo_name = st.text_input("NGO Name", max_chars=100, key="ngo_name")
    description = st.text_area("NGO Description", max_chars=500, key="description")
    email = st.text_input("Contact Email", key="email")
    password = st.text_input("Create Password", type="password", key="password")
    needs = st.text_area("List of Needs (e.g., food, clothes, books)", help="Separate items by commas", key="needs")
    image_logo = st.file_uploader("Upload NGO Logo", type=["jpg", "jpeg", "png"], key="image_logo")
    phone = st.text_input("Contact Phone Number", max_chars=10, key="phone")

    # Custom button styling for Register
    if st.button("Register"):
        if ngo_name and description and email and password and needs:
            # Initialize Firebase and register NGO
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
                if image_logo is not None:
                    image_bytes = image_logo.read()
                else:
                    image_bytes = None
                ngo_db.add_NGO(id_token, ngo_name, "General", image_bytes, description, phone, needs_list, email)

                st.success("NGO Registered Successfully!")
            else:
                st.error("Failed to register. Please try again.")
        else:
            st.error("Please fill in all fields to register.")

if __name__ == "__main__":
    ngo_registration()
