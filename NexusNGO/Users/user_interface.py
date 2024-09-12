import streamlit as st
from PIL import Image
import requests

# Import necessary functions from other modules
from Image_Detection.image_to_text import Response , encode_image
from firebase.firebase_config import initialize_firebase
from firebase.db_interaction import search_ngos_by_items, get_top_ngos
from firebase.storage_interaction import upload_image_to_firebase

def user_ui():
    # Initialize Firebase
    db = initialize_firebase()

    # Set page configuration
    st.set_page_config(page_title="NGO Donation Platform", layout="wide")

    # Custom CSS to enhance the design
    st.markdown("""
        <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
        }
        .title {
            text-align: center;
            color: #2E86C1;
        }
        .sidebar .sidebar-content {
            background-image: linear-gradient(#D6EAF8,#AED6F1);
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("", ["Donate Items", "Donate Funds", "Search NGOs", "Top NGOs"])

    # Main Title
    st.markdown("<h1 class='title'>Welcome to the NGO Donation Platform</h1>", unsafe_allow_html=True)
    st.write("Make a difference by donating items or funds to NGOs in need.")

    if option == "Donate Items":
        donate_items(db)
    elif option == "Donate Funds":
        donate_funds(db)
    elif option == "Search NGOs":
        search_ngos(db)
    elif option == "Top NGOs":
        display_top_ngos(db)

def donate_items(db):
    st.header("Donate Items")
    st.write("You can upload an image of the item or describe it to find matching NGOs.")

    # Option to upload image
    uploaded_image = st.file_uploader("Upload an image of the item", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Upload image to Firebase Storage
        image_url = upload_image_to_firebase(uploaded_image)
        st.success("Image uploaded successfully!")

        # Use AI model to detect objects in the image
        detected_items = Response("image", encode_image(image_url))
        st.write(f"**Detected Items:** {', '.join(detected_items)}")

        # Search for NGOs that need these items
        ngos = search_ngos_by_items(db, detected_items)
        display_ngos(ngos)

    # Option to describe the item
    st.subheader("Or Describe the Item")
    item_description = st.text_area("Describe the item you wish to donate")
    if st.button("Find NGOs"):
        if item_description:
            # Here, you might process the description to extract keywords
            keywords = item_description.split()
            ngos = search_ngos_by_items(db, keywords)
            display_ngos(ngos)
        else:
            st.warning("Please enter a description of the item.")

def donate_funds(db):
    st.header("Donate Funds")
    st.write("Choose an NGO and donate funds securely.")

    # Retrieve list of NGOs from the database
    ngos = get_top_ngos(db)
    ngo_names = [ngo['name'] for ngo in ngos]

    selected_ngo = st.selectbox("Select an NGO to donate to:", ngo_names)
    amount = st.number_input("Enter the amount you wish to donate:", min_value=1.0, step=0.5)

    if st.button("Donate Now"):
        # Process the donation (Blockchain logic to be implemented)
        transaction_id = process_donation(selected_ngo, amount)
        st.success(f"Thank you for your donation! Transaction ID: {transaction_id}")

def search_ngos(db):
    st.header("Search NGOs")
    search_query = st.text_input("Enter keywords to search for NGOs:")
    if st.button("Search"):
        if search_query:
            keywords = search_query.split()
            ngos = search_ngos_by_items(db, keywords)
            display_ngos(ngos)
        else:
            st.warning("Please enter keywords to search.")

def display_top_ngos(db):
    st.header("Top NGOs")
    ngos = get_top_ngos(db)
    display_ngos(ngos)

def display_ngos(ngos):
    if ngos:
        for ngo in ngos:
            st.subheader(ngo['name'])
            st.write(f"**Description:** {ngo['description']}")
            st.write("---")
    else:
        st.write("No NGOs found matching your criteria.")

def process_donation(ngo_name, amount):
    # Implement blockchain transaction logic here
    # Placeholder for transaction ID
    transaction_id = "TXN" + str(hash(f"{ngo_name}{amount}"))
    return transaction_id

# Run the user interface
if __name__ == "__main__":
    user_ui()
