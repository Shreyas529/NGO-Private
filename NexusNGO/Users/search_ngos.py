import streamlit as st
from firebase.firebase_config import initialize_firebase
from firebase.db_interaction import search_ngos_by_items

def search_ngos():
    st.header("Search NGOs")
    st.write("Enter keywords or item names to find relevant NGOs.")

    # Input field for search query
    search_query = st.text_input("Search for NGOs (e.g., clothes, food, books, etc.)")
    
    if st.button("Search"):
        if search_query:
            # Initialize Firebase
            db = initialize_firebase()

            # Split the query into keywords
            keywords = search_query.lower().split()

            # Fetch matching NGOs from Firestore
            ngos = search_ngos_by_items(db, keywords)

            # Display matching NGOs
            display_ngos(ngos)
        else:
            st.warning("Please enter a keyword to search for NGOs.")

def display_ngos(ngos):
    if ngos:
        for ngo in ngos:
            st.subheader(f"NGO: {ngo['name']}")
            st.write(f"**Description**: {ngo['description']}")
            st.write(f"**Needs**: {', '.join(ngo['needs'])}")
            st.write("---")
    else:
        st.write("No NGOs match your search criteria.")

if __name__ == "__main__":
    search_ngos()
