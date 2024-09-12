import streamlit as st
from PIL import Image

# Import necessary functions from other modules
from Image_Detection.image_to_text import Response, encode_image
from Firebase.cred import initialize_firebase
from Firebase.db_interaction import NGO_Database
from Ngos.ngo_interface import display_ngo_dashboard


def user_ui(db):
    # Initialize Firebase
    # db = initialize_firebase()
    ngo_db = NGO_Database(db)

    # Set page configuration
    # st.set_page_config(page_title="NGO Donation Platform", layout="wide")

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
        donate_items(ngo_db)
    elif option == "Donate Funds":
        donate_funds(ngo_db)
    elif option == "Search NGOs":
        search_ngos(ngo_db)
    elif option == "Top NGOs":
        display_top_ngos(ngo_db)

def donate_items(ngo_db):
    st.header("Donate Items")
    st.write("You can upload an image of the item or describe it to find matching NGOs.")

    # Option to upload image
    uploaded_image = st.file_uploader("Upload an image of the item", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Encode and detect objects using the image
        detected_items = Response("image", encode_image(uploaded_image.read())).objects
        st.write(f"**Detected Items:** {', '.join(detected_items)}")

        # Search for NGOs that need these items
        ngos = ngo_db.search_NGO_by_items(detected_items)
        display_ngo_dashboard(ngos)

    # Option to describe the item
    st.subheader("Or Describe the Item")
    item_description = st.text_area("Describe the item you wish to donate")
    if st.button("Find NGOs"):
        if item_description:
            # Process the description to extract keywords
            keywords = item_description.split()
            ngos = ngo_db.search_NGO_by_items(keywords)
            display_ngo_dashboard(ngos)
        else:
            st.warning("Please enter a description of the item.")

def donate_funds(ngo_db):
    st.header("Donate Funds")
    st.write("Choose an NGO and donate funds securely.")

    # Retrieve list of NGOs from the database
    ngos = ngo_db.get_ngos()
    ngo_names = [ngo['Name'] for ngo in ngos]

    selected_ngo = st.selectbox("Select an NGO to donate to:", ngo_names)
    amount = st.number_input("Enter the amount you wish to donate:", min_value=1.0, step=0.5)

    if st.button("Donate Now"):
        # Process the donation (Blockchain logic to be implemented)
        transaction_id = process_donation(selected_ngo, amount)
        st.success(f"Thank you for your donation! Transaction ID: {transaction_id}")

def search_ngos(ngo_db):
    st.header("Search NGOs")
    search_query = st.text_input("Enter keywords to search for NGOs:")
    if st.button("Search"):
        if search_query:
            keywords = search_query.split()
            ngos = ngo_db.search_NGO_by_items(keywords)
            display_ngo_dashboard(ngos)
        else:
            st.warning("Please enter keywords to search.")

def display_top_ngos(ngo_db):
    st.header("Top NGOs")
    ngos = ngo_db.get_ngos()
    for ngo in ngos:
        display_ngo_dashboard(ngo_db,ngo)

def process_donation(ngo_name, amount):
    # Implement blockchain transaction logic here
    # Placeholder for transaction ID
    transaction_id = "TXN" + str(hash(f"{ngo_name}{amount}"))
    return transaction_id

# Run the user interface
if __name__ == "__main__":
    user_ui()
