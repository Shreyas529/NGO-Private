import streamlit as st
from Firebase.cred import initialize_firebase
from Firebase.db_interaction import NGO_Database

def display_top_ngos(db):
    st.header("Top NGOs")

    # Initialize Firebase
    # db = initialize_firebase()
    ngo_db = NGO_Database(db)

    # Get the top NGOs from Firestore database
    ngos = ngo_db.get_top_NGOs()

    if ngos:
        for ngo in ngos:
            # Display each NGO's name and description
            st.subheader(f"NGO: {ngo['Name']}")
            st.write(f"**Description**: {ngo['Description']}")
            st.write(f"**Funds Received**: ${ngo['funds_received']:,}")
            st.write("---")
    else:
        st.write("No NGOs available to display at the moment.")

if __name__ == "__main__":
    display_top_ngos()
