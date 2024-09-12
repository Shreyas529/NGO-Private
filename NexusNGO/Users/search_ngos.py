import streamlit as st
from Firebase.cred import initialize_firebase
from Firebase.db_interaction import NGO_Database

def search_ngos(db):
    st.header("Search NGOs")
    st.write("Enter keywords or item names to find relevant NGOs.")

    # Input field for search query
    search_query = st.text_input("Search for NGOs (e.g., clothes, food, books, etc.)")
    
    if st.button("Search"):
        if search_query:
            # Initialize Firebase
            # db = initialize_firebase()
            ngo_db = NGO_Database(db)

            # Split the query into keywords
            keywords = search_query.lower().split()

            # Fetch matching NGOs from Firestore
            ngos = ngo_db.search_NGO_by_items(keywords)

            # Display matching NGOs
            display_ngos(ngos)
        else:
            st.warning("Please enter a keyword to search for NGOs.")

def display_ngos(ngos):
    if ngos:
        for ngo in ngos:
            st.subheader(f"NGO: {ngo['Name']}")
            st.write(f"**Description**: {ngo['Description']}")
            st.write(f"**Needs**: {', '.join(ngo['needs'])}")
            st.write("---")
    else:
        st.write("No NGOs match your search criteria.")

if __name__ == "__main__":
    search_ngos()
