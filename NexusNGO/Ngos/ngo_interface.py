import streamlit as st
from Firebase.cred import initialize_firebase
from Firebase.authenticate import authenticate_ngo  # Use authenticate function from Firebase/authenticate.py
from Firebase.db_interaction import NGO_Database  # Interact with Firestore data
from Ngos.upldate_ngo import update_profile

# Initialize Firebase globally once
# db = initialize_firebase()

def ngo_interface(db):
    # Apply background and consistent style
    st.markdown("""
    <style>
    body {
        background-color: #0F2027;
        background-image: linear-gradient(315deg, #0F2027 0%, #203A43 74%, #2C5364 100%);
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #60a5fa !important;
    }
    .stButton > button {
        background-color: #FF4B4B !important;  /* Update button color */
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
        background-color: #FFFFFF !important;  /* Hover effect */
        color: #FF4B4B !important;
        transform: scale(1.05);
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['update'] = False
        st.session_state['logged_in'] = False
        st.session_state['ngo_data'] = None
        st.session_state['id_token'] = None

    if st.session_state['logged_in']:
        if st.session_state['update']:
            ngo_db = NGO_Database(db)
            ngo_data = st.session_state['ngo_data']
            update_profile(ngo_db, ngo_data)
        else:
            ngo_db = NGO_Database(db)
            ngo_data = st.session_state['ngo_data']
            display_ngo_dashboard(ngo_db, ngo_data)
    else:
        show_login_form(db)

def show_login_form(db):
    st.markdown("<h2 style='text-align: center; color: #60a5fa;'>NGO Dashboard</h2>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Please login to access your NGO profile.</p>", unsafe_allow_html=True)

    # Login form
    email = st.text_input("Enter your email", key="email_input")
    password = st.text_input("Enter your password", type="password", key="password_input")

    # Custom button styling for login
    if st.button("Login"):
        if email and password:
            ngo_db = NGO_Database(db)

            # Authenticate the NGO
            id_token = authenticate_ngo(email, password)
            
            if id_token:
                ngo_data = get_ngo_data_by_email(ngo_db, email)
                if ngo_data:
                    st.success("Login Successful!")

                    # Store login state in session
                    st.session_state['logged_in'] = True
                    st.session_state['ngo_data'] = ngo_data
                    st.session_state['id_token'] = id_token

                    # Use query params to refresh the page
                    st.experimental_set_query_params(logged_in=True)
                    st.rerun()
                else:
                    st.error("NGO not found in database.")
            else:
                st.error("Login failed. Please check your credentials.")
        else:
            st.warning("Please enter your login details.")

def get_ngo_data_by_email(ngo_db, email):
    ngos_ref = ngo_db.db.collection("NGO").where("email", "==", email).limit(1)
    result = ngos_ref.stream()

    for doc in result:
        return doc.to_dict()

    return None

def display_ngo_dashboard(ngo_db, ngo_data):
    st.subheader(f"Welcome, {ngo_data['Name']}!")
    desc=ngo_data.get('Description', 'No Description').replace("<br>","\n")
    st.write(f"{desc}")
    st.write(f"**Needs**: {', '.join(ngo_data.get('needs', []))}")
    
    # Consistent button styles with hover animation
    if st.button("Update Profile"):
        st.session_state['update'] = True
        st.rerun()

    if st.button("Logout"):
        st.session_state['update'] = False
        st.session_state['logged_in'] = False
        st.session_state['ngo_data'] = None
        st.session_state['id_token'] = None

        # Use query params to refresh the page after logout
        st.experimental_set_query_params(logged_in=False)
        st.rerun()

if __name__ == "__main__":
    ngo_interface()
