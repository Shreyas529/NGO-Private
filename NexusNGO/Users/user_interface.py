import streamlit as st
from PIL import Image

# Import necessary functions from other modules
from Image_Detection.image_to_text import Response, encode_image
from Firebase.cred import initialize_firebase
from Firebase.db_interaction import NGO_Database
from Ngos.ngo_interface import display_ngo_dashboard
from Firebase.db_interaction import ImageDatabase
import base64
import requests
from io import BytesIO
from PIL import Image


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
    # st.markdown("<h1 class='title'>Welcome to the NGO Donation Platform</h1>", unsafe_allow_html=True)
    # st.write("Make a difference by donating items or funds to NGOs in need.")

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
    st.write("You can either upload an image of the item or describe it to find matching NGOs.")

    # Let the user choose between uploading an image or providing a description using selectbox
    option = st.selectbox("Choose your method of donation:", ("Upload an Image", "Describe the Item"))

    if option == "Upload an Image":
        # Option to upload image
        uploaded_image = st.file_uploader("Upload an image of the item", type=["jpg", "jpeg", "png"])

        if uploaded_image:
            # Display the uploaded image
            image = Image.open(uploaded_image)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            buffer = BytesIO()
            image.save(buffer, format="PNG")  # Save the image in buffer
            image_bytes = buffer.getvalue()

            encoded_image = base64.b64encode(image_bytes).decode('utf-8')

            # Encode and detect objects using the image
            response_object = Response("image", encoded_image)
            detected_items = response_object.objects

            st.write(f"**Detected Items:** {', '.join(detected_items)}")

            if st.button("Find NGOs"):
                ngo_data = ngo_db.get_ngos()
                ngo_item_mapping = {ngo_data[i]['Name']: ngo_data[i]['needs'] for i in range(len(ngo_data))}
                resp=response_object._categorise_objects_to_NGO(ngo_item_mapping)
                resp=[resp[i].replace("'","") for i in range(len(resp))]
                markdown_list = "\n".join([f"- {item}" for item in resp])
                st.markdown(markdown_list)
                st.write("Matching NGOs found...")
                
    elif option == "Describe the Item":
        # Option to describe the item
        st.subheader("Describe the Item")
        item_description = st.text_area("Describe the item you wish to donate")
        
        if st.button("Find NGOs"):
            if item_description:
                ngo_data = ngo_db.get_ngos()
                ngo_item_mapping = {ngo_data[i]['Name']: ngo_data[i]['needs'] for i in range(len(ngo_data))}
                # Perform search or matching logic based on item_description
                st.write("Matching NGOs found...")
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
    
    ngos = ngo_db.get_ngos()  # Retrieve list of NGOs from the database
    
    # Iterate through each NGO and display its basic details
    for ngo in ngos:
        
        st.subheader(f"NGO: {ngo['Name']}")
        
        if 'Description' in ngo:
            st.write(f"**Description**: {ngo['Description']}")
        
        if 'Phone' in ngo:
            st.write(f"**Phone**: {ngo['Phone']}")
            
        # if 'Logo' in ngo:
        #     st.image(ngo['Logo'], caption='NGO Logo', use_column_width=True)
        # Handle 'needs' safely, in case the field is missing
        if 'needs' in ngo:
            st.write(f"**Needs**: {', '.join(ngo['needs'])}")
        else:
            st.write("**Needs**: Not specified")
        if "Logo" in ngo:
            image=ImageDatabase().get_image(ngo['Logo'])

            try:
                st.image(image, caption="NGO Logo", use_column_width=True)
            except:
                pass
        
        # st.write(f"**Funds Received**: ${ngo.get('funds_received', 0):,}")
        st.write("---")


def process_donation(ngo_name, amount):
    # Implement blockchain transaction logic here
    # Placeholder for transaction ID
    transaction_id = "TXN" + str(hash(f"{ngo_name}{amount}"))
    return transaction_id

# Run the user interface
if __name__ == "__main__":
    user_ui()
