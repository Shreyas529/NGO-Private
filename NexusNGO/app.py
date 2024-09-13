import streamlit as st
from Firebase.cred import initialize_firebase
from Users.user_interface import user_ui
from Ngos.ngo_interface import ngo_interface
from Ngos.register_ngo import ngo_registration

# Function to display the main page and navigation options
def main():
    # Initialize Firebase once
    db = initialize_firebase()

    # Custom CSS for improved design
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

    # Check if the user role is stored in session_state
    if 'role' not in st.session_state:
        st.session_state['role'] = None

    # If role is not set, display the landing page with role selection
    if st.session_state['role'] is None:
        st.markdown("<h1 class='title'>Welcome to the NGO Donation Platform</h1>", unsafe_allow_html=True)
        st.write("Make a difference by donating items or funds to NGOs in need.")
        
        st.markdown("<h3 class='title'>Please select your role:</h3>", unsafe_allow_html=True)

        # Donor and NGO buttons for navigation
        col1, col2 = st.columns(2)
        with col1:
            donor_button = st.button("I'm a Donor")
        with col2:
            ngo_button = st.button("I'm an NGO")

        # Store the selected role in session_state
        if donor_button:
            st.session_state['role'] = 'Donor'
            st.rerun()  # Immediately rerun to hide the role selection
        elif ngo_button:
            st.session_state['role'] = 'NGO'
            st.rerun()  # Immediately rerun to hide the role selection

    # If role is selected, redirect to respective interface
    if st.session_state['role'] == 'Donor':
        user_ui(db)
    elif st.session_state['role'] == 'NGO':
        ngo_selection(db)

    # Add a "Select Role" option in the sidebar for easy role switching
    if st.session_state['role'] is not None:
        if st.sidebar.button("Select Role"):
            reset_role()
            st.rerun()  # Refresh the app to return to the role selection page

# NGO selection page
def ngo_selection(db):
    st.sidebar.title("NGO Navigation")
    ngo_action = st.sidebar.radio("Select Action", ["Login", "Register NGO"])

    if ngo_action == "Login":
        ngo_interface(db)
    elif ngo_action == "Register NGO":
        ngo_registration(db)

# Function to reset the role and go back to the landing page
def reset_role():
    st.session_state['role'] = None

# Run the main function
if __name__ == "__main__":
    main()
