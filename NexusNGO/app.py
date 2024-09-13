import streamlit as st
from Firebase.cred import initialize_firebase
from Users.user_interface import user_ui
from Ngos.ngo_interface import ngo_interface
from Ngos.register_ngo import ngo_registration

# Custom component for the sidebar
def sidebar(db):
    st.sidebar.title("NGO Navigation")
    ngo_action = st.sidebar.radio("Select Action", ["Login", "Register NGO"])

    if ngo_action == "Login":
        ngo_interface(db)
    elif ngo_action == "Register NGO":
        ngo_registration(db)

# Function to display the main page and navigation options
def main():
    # Initialize Firebase once
    db = initialize_firebase()

    # Custom CSS to add more animations and transitions
    st.markdown("""
        <style>
        /* Global Settings */
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(to bottom, #1e3a8a, #000000);  /* Gradient background */
            color: white;
            margin: 0;
            padding: 0;
        }
        .stApp {
            background: linear-gradient(to bottom, #1e3a8a, #000000);  /* Streamlit App background */
        }
        h1, h3 {
            color: #60a5fa; /* Light blue text */
            text-align: center;
            animation: fadeInDown 1s ease-out;
        }
        h1 {
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            animation: fadeInDown 1s ease-out, pulse 3s infinite;
        }
        h3 {
            font-size: 24px;
            font-weight: 300;
            margin-bottom: 40px;
            animation: fadeInUp 1s ease-out;
        }
        /* Button styling with animation */
        .stButton > button {
            background-color: #3b82f6; /* Blue button */
            color: white;
            border-radius: 30px;
            padding: 10px 24px;
            border: none;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 0 10px;
            width: 200px;
            animation: fadeIn 1.5s ease-out;
        }
        .stButton > button:hover {
            background-color: #60a5fa; /* Light blue on hover */
            transform: scale(1.1); /* Hover scaling */
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
            font-weight: bold;
        }
        .stButton > button:active {
            transform: scale(0.95); /* Tap effect */
        }
        /* Button container for centering */
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 40px;
            gap: 20px;
            animation: fadeInUp 1s ease-out;
        }
        
        /* Adding animation to the content container */
        .content-container {
            background-color: rgba(30, 58, 138, 0.5); /* Transparent blue background */
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
            animation: bounceIn 1s ease-out;
        }

        footer {
            color: #60a5fa;
            text-align: center;
            font-size: 14px;
            margin-top: 50px;
            animation: fadeInUp 1s ease-out;
        }
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes bounceIn {
            0%, 20%, 40%, 60%, 80%, 100% {
                transition-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
            }
            0% {
                opacity: 0;
                transform: scale3d(0.3, 0.3, 0.3);
            }
            20% {
                transform: scale3d(1.1, 1.1, 1.1);
            }
            40% {
                transform: scale3d(0.9, 0.9, 0.9);
            }
            60% {
                opacity: 1;
                transform: scale3d(1.03, 1.03, 1.03);
            }
            80% {
                transform: scale3d(0.97, 0.97, 0.97);
            }
            100% {
                opacity: 1;
                transform: scale3d(1, 1, 1);
            }
        }
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
            100% {
                transform: scale(1);
            }
        }
        </style>
        """, unsafe_allow_html=True)

    # Check if the user role is stored in session_state
    if 'role' not in st.session_state:
        st.session_state['role'] = None

    # If role is not set, display the landing page with role selection
    if st.session_state['role'] is None:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.markdown("<h1>Welcome to NexusNGO</h1>", unsafe_allow_html=True)
        st.markdown("<h3>Connecting donors with NGOs to make a lasting impact.</h3>", unsafe_allow_html=True)

        st.markdown("<h3>Please select your role:</h3>", unsafe_allow_html=True)

        # Donor and NGO buttons for navigation, with centralized layout
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        donor_button = st.button("I'm a Donor")
        ngo_button = st.button("I'm an NGO")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Store the selected role in session_state
        if donor_button:
            st.session_state['role'] = 'Donor'
            st.rerun()  # Immediately rerun to hide the role selection
        elif ngo_button:
            st.session_state['role'] = 'NGO'
            st.rerun()  # Immediately rerun to hide the role selection

    # If role is selected, redirect to respective interface
    if st.session_state['role'] == 'Donor':
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        user_ui(db)
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state['role'] == 'NGO':
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        sidebar(db)
        st.markdown('</div>', unsafe_allow_html=True)

    # Add a "Select Role" option in the sidebar for easy role switching
    if st.session_state['role'] is not None:
        if st.sidebar.button("Select Role"):
            reset_role()
            st.rerun()  # Refresh the app to return to the role selection page

# Function to reset the role and go back to the landing page
def reset_role():
    # Delete all the items in Session state
    for key in st.session_state.keys():
        del st.session_state[key]

# Run the main function
if __name__ == "__main__":
    main()
