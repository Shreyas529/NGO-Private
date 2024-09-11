import streamlit as st
from firebase.firebase_config import initialize_firebase
from firebase.db_interaction import register_ngo

def ngo_registration():
    st.header("NGO Registration")
    st.write("Fill out the form below to register your NGO.")

    # Input fields for NGO registration
    ngo_name = st.text_input("NGO Name", max_chars=100)
    description = st.text_area("NGO Description", max_chars=500)
    email = st.text_input("Contact Email")
    password = st.text_input("Create Password", type="password")
    needs = st.text_area("List of Needs (e.g., food, clothes, books)", help="Separate items by commas")

    if st.button("Register"):
        if ngo_name and description and email and password and needs:
            # Initialize Firebase
            db = initialize_firebase()

            # Prepare data
            needs_list = [item.strip().lower() for item in needs.split(',')]
            ngo_data = {
                "name": ngo_name,
                "description": description,
                "email": email,
                "needs": needs_list,
                "funds_received": 0
            }

            # Register the NGO in Firestore
            register_ngo(db, ngo_data, email, password)
            st.success("NGO Registered Successfully!")
        else:
            st.error("Please fill in all fields to register.")

if __name__ == "__main__":
    ngo_registration()
