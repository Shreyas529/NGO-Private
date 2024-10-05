import streamlit as st
from streamlit_option_menu import option_menu
from Firebase.cred import initialize_firebase
from Users.user_interface import user_ui
from Ngos.ngo_interface import ngo_interface
from Ngos.register_ngo import ngo_registration
from Info.about_us import about_us
from datetime import datetime
import os
# from blockchain.blockchain import get_transactions_last_3_minutes
from Firebase.db_interaction import NGO_Database
from Ngos.upldate_ngo import update_profile
import threading

# Custom component for the sidebar
def sidebar(db):
    if st.session_state.get("logged_in"):
        ngo_interface(db)
    else:
        with st.sidebar:
            ngo_action = option_menu("NGO Navigation", ["Login", "Register NGO", "About-Us"], icons=["box-arrow-in-right", "pencil-square", "info-circle"])
        
        if ngo_action == "Login":
            ngo_interface(db)
        elif ngo_action == "Register NGO":
            ngo_registration(db)
        elif ngo_action == "About-Us":
            about_us()

def check_transactions(db):
    from blockchain.blockchain import get_transactions_last_3_minutes
    print("Checking for transactions")
    ngo_db = NGO_Database(db)
    get_transactions_last_3_minutes([i["metamask_address"] for i in ngo_db.get_ngos()])

def main():
    st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
    """, unsafe_allow_html=True)
    
    db = initialize_firebase()
    
    if st.session_state.get("timestamp") is None:
        st.session_state["timestamp"] = datetime.now()
    
    if (datetime.now() - st.session_state["timestamp"]).seconds > 30:
        st.session_state["timestamp"] = datetime.now()
        # Use threading instead of fork
        thread = threading.Thread(target=check_transactions, args=(db,))
        thread.start()

    st.markdown("""
    <style>
        /* Global Settings */
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(to bottom, #1a202c, #000000);
            color: #f1f1f1;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .stApp {
            background: linear-gradient(to bottom, #1a202c, #000000);
        }
        
        .css-1d391kg {
            background: linear-gradient(to bottom, #1a202c, #000000);
        }
        .css-1d391kg > div {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .css-1d391kg .css-2vl3m9 {
            background-color: transparent;
        }
        .css-2vl3m9 .nav-item {
            text-align: center;
            width: 100%;
        }
        /* Card styling */
        .card {
            display: flex;
            flex: 1 1 auto;
            background-color: #2d3748;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            overflow: hidden;
            max-width: 64rem;
            width: 100%;
            margin: 2rem auto;
        }
        .card-content {
            display: flex;
            flex-direction: column;
        }
        @media (min-width: 768px) {
            .card-content {
                flex-direction: row;
            }
        }
        .image-container {
            flex: 1;
            padding-top: 6.1rem;
        }
        .image-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .text-container {
            flex: 1;
            padding: 2rem;
        }
        .card h1, .card h3 {
            color: #e5e5e5;
        }
        /* Button styling */
        .stButton > button {
            background-color: #FF4B4B;
            color: white;
            border-radius: 9999px;
            padding: 0.5rem 1rem;
            border: none;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 0.5rem 0;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #FFFFFF;
            color: #FF4B4B;
            transform: scale(1.05);
        }
    </style>
    """, unsafe_allow_html=True)

    if 'role' not in st.session_state:
        st.session_state['role'] = None

    if st.session_state['role'] is None:
        col1, col2 = st.columns(2, gap='medium')
        
        with col1:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image("./test.jpg")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="text-container">', unsafe_allow_html=True)
            st.markdown("<h1>Welcome to NexusNGO</h1>", unsafe_allow_html=True)
            st.markdown("<h3>Connecting donors with NGOs to make a lasting impact.</h3>", unsafe_allow_html=True)
            st.markdown("<h3>Please select your role:</h3>", unsafe_allow_html=True)
            
            donor_button = st.button("I'm a Donor")
            ngo_button = st.button("I'm an NGO")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if donor_button:
            st.session_state['role'] = 'Donor'
            st.rerun()
        elif ngo_button:
            st.session_state['role'] = 'NGO'
            st.rerun()

    if st.session_state['role'] == 'Donor':
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        user_ui(db)
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state['role'] == 'NGO':
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        sidebar(db)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state['role'] is not None:
        if st.sidebar.button("Select Role"):
            reset_role()
            st.rerun()

def reset_role():
    for key in st.session_state.keys():
        del st.session_state[key]

if __name__ == "__main__":
    main()
