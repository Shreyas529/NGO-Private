import streamlit as st
from Firebase.cred import initialize_firebase
from Firebase.authenticate import authenticate_ngo  # Use authenticate function from Firebase/authenticate.py
from Firebase.db_interaction import NGO_Database  # Interact with Firestore data

def ngo_interface(db):
    st.header("NGO Dashboard")

    # Login form
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Login"):
        if email and password:
            # Initialize Firebase
            # db = initialize_firebase()
            ngo_db = NGO_Database(db)

            # Authenticate the NGO
            id_token = authenticate_ngo(email, password)
            
            if id_token:
                st.success("Login Successful!")
                ngo_data = get_ngo_data_by_email(ngo_db, email)
                if ngo_data:
                    display_ngo_dashboard(ngo_db, ngo_data)
                else:
                    st.error("NGO not found in database.")
            else:
                st.error("Login failed. Please check your credentials.")
        else:
            st.warning("Please enter your login details.")

def get_ngo_data_by_email(ngo_db, email):
    """
    Fetch the NGO data using the email.
    :param ngo_db: NGO_Database instance
    :param email: NGO email
    :return: NGO data if found, None if not found
    """
    ngos_ref = ngo_db.db.collection("NGO").where("email", "==", email).limit(1)
    result = ngos_ref.stream()

    for doc in result:
        return doc.to_dict()

    return None

def display_ngo_dashboard(ngo_db, ngo_data):
    """
    Display the NGO's dashboard with their profile details and options to update.
    :param ngo_db: NGO_Database instance
    :param ngo_data: The logged-in NGO's data
    """
    st.subheader(f"Welcome, {ngo_data['Name']}!")
    st.write(f"**Description**: {ngo_data['Description']}")
    st.write(f"**Needs**: {', '.join(ngo_data['needs'])}")
    st.write(f"**Funds Received**: ${ngo_data['funds_received']:,}")
    
    # Option to update NGO profile
    if st.button("Update Profile"):
        update_profile(ngo_db, ngo_data)

def update_profile(ngo_db, ngo_data):
    st.subheader("Update Profile")

    # Input fields pre-filled with current data
    new_description = st.text_area("Update Description", value=ngo_data['Description'])
    new_needs = st.text_area("Update Needs", value=", ".join(ngo_data['needs']))

    if st.button("Submit Changes"):
        # Prepare updated data
        updated_needs = [item.strip().lower() for item in new_needs.split(",")]

        # Update Firestore with new data
        ngo_data['Description'] = new_description
        ngo_data['needs'] = updated_needs

        ngo_db.update_NGO_Description(ngo_data['Name'], new_description)
        ngo_db.update_NGO_Needs(ngo_data['Name'], updated_needs)
        st.success("Profile updated successfully!")

if __name__ == "__main__":
    ngo_interface()
