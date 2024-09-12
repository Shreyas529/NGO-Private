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

    # Sidebar navigation
    st.sidebar.title("Navigation")
    user_type = st.sidebar.radio("Select User Type", ["User", "NGO", "Register NGO"])

    # Main Title
    st.markdown("<h1 class='title'>Welcome to the NGO Donation Platform</h1>", unsafe_allow_html=True)
    st.write("Make a difference by donating items or funds to NGOs in need.")

    # User selection: User Interface, NGO Interface, or Register NGO
    if user_type == "User":
        user_ui(db)
    elif user_type == "NGO":
        ngo_interface(db)
    elif user_type == "Register NGO":
        ngo_registration(db)

# Run the main function
if __name__ == "__main__":
    main()
