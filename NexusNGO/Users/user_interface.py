import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import pandas as pd

# Import necessary functions from other modules
from Image_Detection.image_to_text import Response, encode_image
from streamlit_option_menu import option_menu
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
            background-color: #FF4B4B; /* Consistent color with app.py */
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
            color: #FF4B4B;
            transform: scale(1.05);
            font-weight: bold;
        }
        a.ngo-link {
            color: #FFFFFF;
            font-weight: bold;
            text-decoration: none;
        }
        a.ngo-link:hover {
            color: #60a5fa;
            text-decoration: underline;
            cursor: pointer;
        }
        .ngo-container {
            background-color: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        # option = st.sidebar.radio("", ["Donate Items", "Donate Funds", "Search NGOs", "Top NGOs"], key="nav_option")
        option = option_menu("Donor Navigation",["Donate Items", "Donate Funds", "Search NGOs", "Top NGOs"] ,icons=["gift", "cash" , "search" , "bar-chart"],key="nav_option")

    if option == "Donate Items":
        donate_items(ngo_db)
    elif option == "Donate Funds":
        donate_funds(ngo_db)
    elif option == "Search NGOs":
        search_ngos(ngo_db)
    elif option == "Top NGOs":
        display_top_ngos(ngo_db)


def donate_items(ngo_db):
    st.markdown("<h1>👐 Donate Items</h1>", unsafe_allow_html=True)
    st.write("You can either upload an image of the item or describe it to find matching NGOs.")

    option = st.selectbox("How would you like to proceed?", ("📸 Upload an Image", "📝 Describe the Item"))

    if option == "📸 Upload an Image":
        st.subheader("Upload an Image of the Item")
        uploaded_image = st.file_uploader("Upload an image of the item (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption='🖼 Uploaded Image', use_column_width=True)

            # Process the image
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')

            if st.button("🔍 Find Matching NGOs"):
                response_object = Response("image", encoded_image)
                detected_items = response_object.objects
                st.markdown(f"<h3 style='color: #FF4B4B;'>🔍 Detected Items: {', '.join(detected_items)}</h3>", unsafe_allow_html=True)

                ngo_data = ngo_db.get_ngos()
                ngo_item_mapping = {ngo['Name']: ngo['needs'] for ngo in ngo_data}
                resp = response_object._categorise_objects_to_NGO(ngo_item_mapping)
                resp = [ngo_name.replace("'", "") for ngo_name in resp if ngo_name]

                if resp:
                    data = {"NGO Name": resp}
                    data["Contact"] = [ngo['Phone'] for ngo in ngo_data if ngo['Name'] in data["NGO Name"]]
                    data["Email"] = [ngo['email'] for ngo in ngo_data if ngo['Name'] in data["NGO Name"]]
                    df = pd.DataFrame(data)

                    # Display NGOs with expander for additional details
                    for index, row in df.iterrows():
                        ngo_name = row['NGO Name']
                        contact = row['Contact']
                        email = row['Email']
                        st.markdown(f"### {index + 1}: {ngo_name}")
                        st.write(f"📞 Contact: {contact}")
                        st.write(f"📧 Email: {email}")

                        # Use an expander for needs and description
                        with st.expander(f"More details about {ngo_name}"):
                            ngo_details = next(ngo for ngo in ngo_data if ngo['Name'] == ngo_name)
                            st.write(f"**Needs**: {', '.join(ngo_details.get('needs', []))}")
                            st.write(f"**Description**: {ngo_details.get('Description', 'No description available')}")

                        # Button to view more details
                        # if st.button(f"View More: {ngo_name}", key=f"view_more_{index}"):
                        #     st.session_state['selected_ngo'] = ngo_name
                        #     st.rerun()  # Reload the UI to show the NGO page


def describe_item(ngo_db):
    st.subheader("Describe the Item You Wish to Donate")
    item_description = st.text_area("📝 Describe the item you wish to donate", height=150, max_chars=300)

    if st.button("🔍 Find Matching NGOs"):
        if item_description:
            response_object = Response("text", item_description)
            detected_items = response_object.objects
            st.markdown(f"<h3 style='color: #FF4B4B;'>🔍 Detected Items: {', '.join(detected_items)}</h3>", unsafe_allow_html=True)

            ngo_data = ngo_db.get_ngos()
            ngo_item_mapping = {ngo['Name']: ngo['needs'] for ngo in ngo_data}
            resp = response_object._categorise_objects_to_NGO(ngo_item_mapping)
            resp = [ngo_name.replace("'", "") for ngo_name in resp]

            if resp:
                data = {"NGO Name": resp}
                data["Contact"] = [ngo['Phone'] for ngo in ngo_data if ngo['Name'] in data["NGO Name"]]
                data["Email"] = [ngo['email'] for ngo in ngo_data if ngo['Name'] in data["NGO Name"]]
                df = pd.DataFrame(data)

                # Display NGOs with expander for additional details
                for index, row in df.iterrows():
                    ngo_name = row['NGO Name']
                    contact = row['Contact']
                    email = row['Email']
                    st.markdown(f"### {index + 1}: {ngo_name}")
                    st.write(f"📞 Contact: {contact}")
                    st.write(f"📧 Email: {email}")

                    # Use an expander for needs and description
                    with st.expander(f"More details about {ngo_name}"):
                        ngo_details = next(ngo for ngo in ngo_data if ngo['Name'] == ngo_name)
                        st.write(f"**Needs**: {', '.join(ngo_details.get('needs', []))}")
                        st.write(f"**Description**: {ngo_details.get('Description', 'No description available')}")

                    # Button to view more details
                    # if st.button(f"View More: {ngo_name}", key=f"view_more_{index}"):
                    #     st.session_state['selected_ngo'] = ngo_name
                    #     st.rerun()  # Reload the UI to show the NGO page


def display_selected_ngo(ngo_db, ngo_name):
    # Fetch NGO details from the database
    ngo_details = ngo_db.get_ngo_by_name(ngo_name)

    st.markdown(f"<h2>Details for {ngo_name}</h2>", unsafe_allow_html=True)
    st.write(f"**Description**: {ngo_details.get('Description', 'No description available')}")
    st.write(f"**Phone**: {ngo_details.get('Phone', 'No phone available')}")
    if 'Logo' in ngo_details:
        logo = ImageDatabase().get_image(ngo_details['Logo'])
        st.image(logo, caption=f"{ngo_name} Logo", use_column_width=True)

    st.write(f"**Needs**: {', '.join(ngo_details.get('needs', []))}")

    # Back to the results
    if st.button("Back to Results"):
        del st.session_state['selected_ngo']  # Remove selected NGO from session state
        st.experimental_rerun()  # Reload the UI to go back to the previous page


def donate_funds(ngo_db):
    st.markdown("<h1 class='header section-header fade-in'>💰 Donate Funds</h1>", unsafe_allow_html=True)
    st.write("Choose an NGO and securely donate funds.")

    # Donation Section
    ngos = ngo_db.get_ngos()
    ngo_names = [ngo['Name'] for ngo in ngos]
    selected_ngo = st.selectbox("Select an NGO to donate to:", ngo_names)

    amount = st.number_input("Enter the amount you wish to donate:", min_value=1.0, step=0.5)

    if st.button("Donate Now") and selected_ngo is not None and amount > 0:
        transaction_id = process_donation(selected_ngo, amount)
        st.success(f"Thank you for your donation! Transaction ID: {transaction_id}")


def search_ngos(ngo_db):
    st.markdown("<h1>🔍 Search NGOs by Name</h1>", unsafe_allow_html=True)
    search_query = st.text_input("Search for NGOs by name:")

    if search_query:
        ngo_data = ngo_db.get_ngos()  # Fetch all NGO data
        filtered_ngos = [ngo for ngo in ngo_data if search_query.lower() in ngo['Name'].lower()]

        if filtered_ngos:
            for ngo in filtered_ngos:
                ngo_name = ngo['Name']
                ngo_phone = ngo.get('Phone', 'No phone available')
                ngo_email = ngo.get('email', 'No email available')

                with st.expander(f"{ngo_name}"):
                    st.markdown(f"""
                    <p><strong>Phone:</strong> {ngo_phone}</p>
                    <p><strong>Email:</strong> {ngo_email}</p>
                    <p><strong>Description:</strong> {ngo.get('Description', 'No description available')}</p>
                    <p><strong>Needs:</strong> {', '.join(ngo.get('needs', []))}</p>
                    """, unsafe_allow_html=True)
        else:
            st.write("No NGOs found with that name.")


def display_top_ngos(ngo_db):
    st.markdown("<h1 class='header section-header fade-in'>🌟 Top NGOs</h1>", unsafe_allow_html=True)
    
    ngos = ngo_db.get_ngos()
    for ngo in ngos:
        st.markdown(f"<h3 class='fade-in-slow'>NGO: {ngo['Name']}</h3>", unsafe_allow_html=True)
        st.write(f"*Description*: {ngo.get('Description', 'No description available')}")
        st.write(f"*Phone*: {ngo.get('Phone', 'No phone available')}")

        if 'Logo' in ngo:
            image = ImageDatabase().get_image(ngo['Logo'])
            st.image(image, caption="NGO Logo", use_column_width=True)
        st.write(f"*Needs*: {', '.join(ngo.get('needs', []))}")
        st.write("---")


def process_donation(ngo_name, amount):
    transaction_id = "TXN" + str(hash(f"{ngo_name}{amount}"))
    return transaction_id


# Run the user interface
if __name__ == "__main__":
    user_ui()

