import streamlit as st
from firebase.firebase_config import initialize_firebase
from firebase.db_interaction import get_ngo_data, update_ngo_profile

def ngo_interface():
    st.header("NGO Dashboard")

    # Login form
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Login"):
        if email and password:
            # Initialize Firebase
            db = initialize_firebase()

            # Authenticate the NGO
            ngo_data = authenticate_ngo(db, email, password)
            
            if ngo_data:
                st.success("Login Successful!")
                display_ngo_dashboard(db, ngo_data)
            else:
                st.error("Login failed. Please check your credentials.")
        else:
            st.warning("Please enter your login details.")

def authenticate_ngo(db, email, password):
    """
    Authenticate the NGO using Firebase Authentication.
    :param db: Firebase client instance
    :param email: NGO email
    :param password: NGO password
    :return: NGO data if authenticated, None if authentication fails
    """
    auth = db.auth()
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # Fetch the NGO data from Firestore
        ngos_ref = db.collection("ngos").where("email", "==", email).limit(1)
        result = ngos_ref.stream()

        for doc in result:
            return doc.to_dict()

    except:
        return None

def display_ngo_dashboard(db, ngo_data):
    """
    Display the NGO's dashboard with their profile details and options to update.
    :param db: Firestore client instance
    :param ngo_data: The logged-in NGO's data
    """
    st.subheader(f"Welcome, {ngo_data['name']}!")
    st.write(f"**Description**: {ngo_data['description']}")
    st.write(f"**Needs**: {', '.join(ngo_data['needs'])}")
    st.write(f"**Funds Received**: ${ngo_data['funds_received']:,}")
    
    # Option to update NGO profile
    if st.button("Update Profile"):
        update_profile(db, ngo_data)

def update_profile(db, ngo_data):
    st.subheader("Update Profile")

    # Input fields pre-filled with current data
    new_description = st.text_area("Update Description", value=ngo_data['description'])
    new_needs = st.text_area("Update Needs", value=", ".join(ngo_data['needs']))

    if st.button("Submit Changes"):
        # Prepare updated data
        updated_needs = [item.strip().lower() for item in new_needs.split(",")]

        # Update Firestore with new data
        ngo_data['description'] = new_description
        ngo_data['needs'] = updated_needs

        update_ngo_profile(db, ngo_data)
        st.success("Profile updated successfully!")

if __name__ == "__main__":
    ngo_interface()
