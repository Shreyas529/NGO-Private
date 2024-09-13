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
import pandas as pd


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

import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def donate_items(ngo_db):
    # Page header
    st.markdown("<h1 style='text-align: center; color: #FF6F61;'>👐 Donate Items</h1>", unsafe_allow_html=True)
    st.write("You can either upload an image of the item or describe it to find matching NGOs.")

    # Choose method of donation (image or description)
    option = st.selectbox(
        "How would you like to proceed?",
        ("📸 Upload an Image", "📝 Describe the Item")
    )

    if option == "📸 Upload an Image":
        # Image upload option
        st.subheader("Upload an Image of the Item")
        uploaded_image = st.file_uploader("Upload an image of the item (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

        if uploaded_image:
            # Display uploaded image
            image = Image.open(uploaded_image)
            st.image(image, caption='🖼 Uploaded Image', use_column_width=True)
            
            # Convert image to base64 for processing
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')

            # Process image (object detection)
        

            # Display detected items

            # Button to find matching NGOs
            if st.button("🔍 Find Matching NGOs"):
            
                response_object=Response("image",encoded_image)
                detected_items = response_object.objects
                st.markdown(f"<h3 style='color: #333;'>🔍 Detected Items: {', '.join(detected_items)}</h3>", unsafe_allow_html=True)
                ngo_data = ngo_db.get_ngos()
                ngo_item_mapping = {ngo_data[i]['Name']: ngo_data[i]['needs'] for i in range(len(ngo_data))}
                resp = response_object._categorise_objects_to_NGO(ngo_item_mapping)
                resp = [resp[i].replace("'", "") for i in range(len(resp)) if resp[i]!=""]
                

                data = {"NGO Name": resp}
                data["Contact"] = [ngo_data[i]['Phone'] for i in range(len(ngo_data)) if ngo_data[i]['Name'] in data["NGO Name"]]
                print(data)
                df = pd.DataFrame(data)

                # Apply styling to the DataFrame
                styled_df = df.style.set_properties(**{
                    'background-color': '#f5f5f5',
                    'color': '#333',
                    'border-color': '#FF6F61',
                    'border-width': '2px',
                    'border-style': 'solid',
                    'text-align': 'left'
                }).set_table_styles([
                    {
                        'selector': 'thead th',
                        'props': [('background-color', '#FF6F61'), ('color', 'white')]
                    }
                ])

                st.markdown("<h3 style='color: #FF6F61;'>🎯 Matching NGOs Found:</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 2, 1])
                col1.markdown("**NGO Name**")
                col2.markdown("**Contact**")
                col3.markdown("")

                # Display each row in the table with a "View More" button
                for i, row in df.iterrows():
                    ngo = ngo_data[i]
                    col1, col2, col3 = st.columns([3, 2, 1])

                    col1.write(row["NGO Name"])
                    col2.write(row["Contact"])
                    
                    if col3.button("View More", key=row["NGO Name"]):
                        st.session_state.selected_ngo = ngo  # Save selected NGO details in session state
                        st.rerun()  # Refresh to navigate to the details page
            


    
    elif option == "📝 Describe the Item":
        # Description option
        st.subheader("Describe the Item You Wish to Donate")
        item_description = st.text_area("📝 Describe the item you wish to donate", height=150, max_chars=300)
        
        
        # Button to find NGOs based on description
        if st.button("🔍 Find Matching NGOs"):
            if item_description:
                response_object=Response("text",item_description)
                detected_items = response_object.objects
                st.markdown(f"<h3 style='color: #333;'>🔍 Detected Items: {', '.join(detected_items)}</h3>", unsafe_allow_html=True)
            if item_description:
                ngo_data = ngo_db.get_ngos()
                ngo_item_mapping = {ngo_data[i]['Name']: ngo_data[i]['needs'] for i in range(len(ngo_data))}
                resp = response_object._categorise_objects_to_NGO(ngo_item_mapping)
                resp = [resp[i].replace("'", "") for i in range(len(resp))]

                data = {"NGO Name": resp}
                data["Contact"] = [ngo_data[i]['Phone'] for i in range(len(ngo_data)) if ngo_data[i]['Name'] in data["NGO Name"]]

                df = pd.DataFrame(data)

                # Apply styling to the DataFrame
                styled_df = df.style.set_properties(**{
                    'background-color': '#f5f5f5',
                    'color': '#333',
                    'border-color': '#FF6F61',
                    'border-width': '2px',
                    'border-style': 'solid',
                    'text-align': 'left'
                }).set_table_styles([
                    {
                        'selector': 'thead th',
                        'props': [('background-color', '#FF6F61'), ('color', 'white')]
                    }
                ])

                st.markdown("<h3 style='color: #FF6F61;'>🎯 Matching NGOs Found:</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 2, 1])
                col1.markdown("**NGO Name**")
                col2.markdown("**Contact**")
                col3.markdown("")

                # Display each row in the table with a "View More" button
                for i, row in df.iterrows():
                    ngo = ngo_data[i]
                    col1, col2, col3 = st.columns([3, 2, 1])

                    col1.write(row["NGO Name"])
                    col2.write(row["Contact"])
                    
                if col3.button("View More", key=row["NGO Name"]):
                    st.session_state.selected_ngo = ngo  # Save selected NGO details in session state
                    st.rerun()  # Refresh to navigate to the details page
            else:
                st.warning("⚠️ Please enter a description of the item.")


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
