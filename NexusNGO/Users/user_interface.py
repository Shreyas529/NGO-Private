import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import pandas as pd

# Import necessary functions from other modules
from Image_Detection.image_to_text import Response, encode_image
from Firebase.cred import initialize_firebase
from Firebase.db_interaction import NGO_Database
from Firebase.db_interaction import ImageDatabase
from Ngos.ngo_interface import display_ngo_dashboard


def user_ui(db):
    # Initialize Firebase
    ngo_db = NGO_Database(db)

    # Apply custom CSS for consistent design and animation
    st.markdown("""
        <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .stButton > button {
            background-color: #FF6F61; /* Consistent color with app.py */
            color: white;
            border-radius: 30px;
            padding: 10px 24px;
            border: none;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 0 10px;
            width: 200px;
        }
        .stButton > button:hover {
            background-color: #FFFFFF; /* Hover effect */
            color: #FF6F61;
            transform: scale(1.05);
            font-weight: bold;
        }
        .header {
            text-align: center;
            color: #60a5fa;
            animation: fadeInDown 1s ease-out;
        }
        .section-header {
            font-size: 36px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        .sidebar-content {
            background-image: linear-gradient(#D6EAF8,#AED6F1);
            color: white;
        }
        .fade-in {
            animation: fadeIn 2s ease-in-out;
        }
        .fade-in-slow {
            animation: fadeIn 3s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar navigation with fade-in effect
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("", ["Donate Items", "Donate Funds", "Search NGOs", "Top NGOs"], key="nav_option")

    if option == "Donate Items":
        donate_items(ngo_db)
    elif option == "Donate Funds":
        donate_funds(ngo_db)
    elif option == "Search NGOs":
        search_ngos(ngo_db)
    elif option == "Top NGOs":
        display_top_ngos(ngo_db)

# Update "Donate Items" function with consistent animations and styles
def donate_items(ngo_db):
    # Page header with fade-in effect
    st.markdown("<h1 class='fade-in' style='text-align: center; color: #60a5fa;'>👐 Donate Items</h1>", unsafe_allow_html=True)
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

            # Button to find matching NGOs with animation
            if st.button("🔍 Find Matching NGOs"):
                response_object = Response("image", encoded_image)
                detected_items = response_object.objects
                st.markdown(f"<h3 class='fade-in-slow' style='color: #FF6F61;'>🔍 Detected Items: {', '.join(detected_items)}</h3>", unsafe_allow_html=True)
                
                ngo_data = ngo_db.get_ngos()
                ngo_item_mapping = {ngo_data[i]['Name']: ngo_data[i]['needs'] for i in range(len(ngo_data))}
                resp = response_object._categorise_objects_to_NGO(ngo_item_mapping)
                resp = [resp[i].replace("'", "") for i in range(len(resp)) if resp[i] != ""]
                data = {"NGO Name": resp}
                data["Contact"] = [ngo_data[i]['Phone'] for i in range(len(ngo_data)) if ngo_data[i]['Name'] in data["NGO Name"]]
                df = pd.DataFrame(data)

                # Display matching NGOs
                st.markdown("<h3 class='fade-in' style='color: #FF6F61;'>🎯 Matching NGOs Found:</h3>", unsafe_allow_html=True)
                st.dataframe(df)

    elif option == "📝 Describe the Item":
        st.subheader("Describe the Item You Wish to Donate")
        item_description = st.text_area("📝 Describe the item you wish to donate", height=150, max_chars=300)

        # Button to find NGOs based on description
        if st.button("🔍 Find Matching NGOs"):
            if item_description:
                response_object = Response("text", item_description)
                detected_items = response_object.objects
                st.markdown(f"<h3 class='fade-in' style='color: #FF6F61;'>🔍 Detected Items: {', '.join(detected_items)}</h3>", unsafe_allow_html=True)
                
                ngo_data = ngo_db.get_ngos()
                ngo_item_mapping = {ngo_data[i]['Name']: ngo_data[i]['needs'] for i in range(len(ngo_data))}
                resp = response_object._categorise_objects_to_NGO(ngo_item_mapping)
                resp = [resp[i].replace("'", "") for i in range(len(resp))]
                data = {"NGO Name": resp}
                data["Contact"] = [ngo_data[i]['Phone'] for i in range(len(ngo_data)) if ngo_data[i]['Name'] in data["NGO Name"]]
                df = pd.DataFrame(data)
                st.markdown("<h3 class='fade-in' style='color: #FF6F61;'>🎯 Matching NGOs Found:</h3>", unsafe_allow_html=True)
                st.dataframe(df)
            else:
                st.warning("⚠️ Please enter a description of the item.")

def donate_funds(ngo_db):
    st.markdown("<h1 class='header section-header fade-in'>💰 Donate Funds</h1>", unsafe_allow_html=True)
    st.write("Choose an NGO and securely donate funds.")

    ngos = ngo_db.get_ngos()
    ngo_names = [ngo['Name'] for ngo in ngos]
    selected_ngo = st.selectbox("Select an NGO to donate to:", ngo_names)

    amount = st.number_input("Enter the amount you wish to donate:", min_value=1.0, step=0.5)

    if st.button("Donate Now") and selected_ngo is not None and amount > 0:
        transaction_id = process_donation(selected_ngo, amount)
        st.success(f"Thank you for your donation! Transaction ID: {transaction_id}")

def search_ngos(ngo_db):
    st.markdown("<h1 class='header section-header fade-in'>🔍 Search NGOs</h1>", unsafe_allow_html=True)
    search_query = st.text_input("Enter keywords to search for NGOs:")
    if st.button("Search"):
        if search_query:
            keywords = search_query.split()
            ngos = ngo_db.search_NGO_by_items(keywords)
            display_ngo_dashboard(ngos)
        else:
            st.warning("⚠️ Please enter keywords to search.")

def display_top_ngos(ngo_db):
    st.markdown("<h1 class='header section-header fade-in'>🌟 Top NGOs</h1>", unsafe_allow_html=True)
    
    ngos = ngo_db.get_ngos()
    for ngo in ngos:
        st.markdown(f"<h3 class='fade-in-slow'>NGO: {ngo['Name']}</h3>", unsafe_allow_html=True)
        st.write(f"**Description**: {ngo.get('Description', 'No description available')}")
        st.write(f"**Phone**: {ngo.get('Phone', 'No phone available')}")

        if 'Logo' in ngo:
            image = ImageDatabase().get_image(ngo['Logo'])
            st.image(image, caption="NGO Logo", use_column_width=True)
        st.write(f"**Needs**: {', '.join(ngo.get('needs', []))}")
        st.write("---")

def process_donation(ngo_name, amount):
    transaction_id = "TXN" + str(hash(f"{ngo_name}{amount}"))
    return transaction_id

# Run the user interface
if __name__ == "__main__":
    user_ui()

