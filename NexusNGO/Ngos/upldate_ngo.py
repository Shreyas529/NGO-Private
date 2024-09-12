import streamlit as st
from Firebase.db_interaction import NGO_Database # Interact with Firestore data

        
def update_profile(ngo_db, ngo_data):
    st.subheader("Update Profile")

    # Input fields pre-filled with current data
    new_description = st.text_area("Update Description", value=ngo_data.get('Description', ''))
    new_needs = st.text_area("Update Needs", value=", ".join(ngo_data.get('needs', [])))

    if st.button("Submit Changes"):
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