import streamlit as st
from firebase.firebase_config import initialize_firebase
from firebase.db_interaction import get_top_ngos

def display_top_ngos():
    st.header("Top NGOs")

    # Initialize Firebase
    db = initialize_firebase()

    # Get the top NGOs from the Firebase Firestore database
    ngos = get_top_ngos(db)

    if ngos:
        for ngo in ngos:
            # Display each NGO's name and description
            st.subheader(f"NGO: {ngo['name']}")
            st.write(f"**Description**: {ngo['description']}")
            st.write(f"**Funds Received**: ${ngo['funds_received']:,}")
            st.write("---")
    else:
        st.write("No NGOs available to display at the moment.")

if __name__ == "__main__":
    display_top_ngos()
