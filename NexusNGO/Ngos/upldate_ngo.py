import streamlit as st
from Firebase.db_interaction import NGO_Database  # Interact with Firestore data

def update_profile(ngo_db, ngo_data):
    # Centered header with animation
    st.markdown("<h2 class='fade-in'>Update Profile</h2>", unsafe_allow_html=True)

    # Input fields with current data and animation
    new_description = st.text_area(
        "Update Description",
        value=ngo_data.get('Description', ''),
        height=150,
        max_chars=500,
        help="Please update the description of your NGO here.",
    )
    new_needs = st.text_area(
        "Update Needs",
        value=", ".join(ngo_data.get('needs', [])),
        height=150,
        max_chars=300,
        help="Specify the needs separated by commas."
    )

    # Custom button style with animations
    if st.button("Submit Changes", key='submit_button'):
        # Prepare updated data
        updated_needs = [item.strip().lower() for item in new_needs.split(",")]

        # Update Firestore with new data
        ngo_db.update_NGO_Description(st.session_state['id_token'], ngo_data['Name'], new_description)
        ngo_db.update_NGO_Needs(st.session_state['id_token'], ngo_data['Name'], updated_needs)

        # Update session data with new values
        ngo_data['Description'] = new_description
        ngo_data['needs'] = updated_needs
        st.session_state['ngo_data'] = ngo_data

        st.success("Profile updated successfully!")
        st.session_state['update'] = False
        st.experimental_set_query_params(updated=True)  # Refresh the page to show the updated profile
        st.rerun()

st.markdown("""
<style>
    .st-bx {
        box-shadow: none;
        background-color: #f1f8ff;
        border-color: #AED6F1;
        border-radius: 15px;
    }
    .stButton > button {
        background-color: #FF6F61 !important; /* Ensure the button uses the correct color */
        color: white !important;
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
        background-color: #FFFFFF !important; /* Ensure hover effect works */
        color: #FF6F61 !important;
        transform: scale(1.05);
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
