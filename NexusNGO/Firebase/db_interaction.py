def register_ngo(db, ngo_data, email, password):
    """
    Register a new NGO in Firestore and Firebase Authentication.
    :param db: Firestore client instance
    :param ngo_data: NGO data to store in Firestore
    :param email: Email for authentication
    :param password: Password for authentication
    """
    # Create a new user in Firebase Authentication
    auth = db.auth()
    try:
        user = auth.create_user_with_email_and_password(email, password)

        # Add NGO data to Firestore
        ngos_ref = db.collection("ngos")
        ngos_ref.add(ngo_data)
        print("NGO registered successfully!")
    except Exception as e:
        print(f"Error registering NGO: {e}")

def authenticate_ngo(db, email, password):
    """
    Authenticate the NGO using Firebase Authentication.
    :param db: Firebase client instance
    :param email: NGO email
    :param password: NGO password
    :return: NGO data if authenticated, None if authentication fails
    """
    auth = db.auth()
    try:
        # Sign in the user with email and password
        user = auth.sign_in_with_email_and_password(email, password)

        # Fetch the NGO data from Firestore
        ngos_ref = db.collection("ngos").where("email", "==", email).limit(1)
        result = ngos_ref.stream()

        for doc in result:
            return doc.to_dict()

    except Exception as e:
        print(f"Error during NGO authentication: {e}")
        return None

def get_top_ngos(db):
    """
    Fetch top NGOs from Firestore, sorted by funds received.
    :param db: Firestore client instance
    :return: List of top NGOs
    """
    ngos_ref = db.collection("ngos")
    query = ngos_ref.order_by("funds_received", direction="DESCENDING").limit(5)
    results = query.stream()

    ngos = []
    for doc in results:
        ngo_data = doc.to_dict()
        ngos.append({
            'name': ngo_data.get('name', 'N/A'),
            'description': ngo_data.get('description', 'No description available'),
            'funds_received': ngo_data.get('funds_received', 0)
        })

    return ngos

def search_ngos_by_items(db, keywords):
    """
    Search for NGOs that match the provided keywords (needs).
    :param db: Firestore client instance
    :param keywords: List of keywords to match NGO needs
    :return: List of matching NGOs
    """
    ngos_ref = db.collection("ngos")
    ngos = []

    for keyword in keywords:
        query = ngos_ref.where("needs", "array_contains", keyword)
        results = query.stream()

        for doc in results:
            ngo_data = doc.to_dict()
            ngos.append({
                'name': ngo_data.get('name', 'N/A'),
                'description': ngo_data.get('description', 'No description available'),
                'needs': ngo_data.get('needs', [])
            })

    return ngos

def update_ngo_profile(db, ngo_data):
    """
    Update an NGO's profile in Firestore.
    :param db: Firestore client instance
    :param ngo_data: Updated NGO data to store
    """
    ngos_ref = db.collection("ngos").where("email", "==", ngo_data['email']).limit(1)
    results = ngos_ref.stream()

    for doc in results:
        doc_ref = db.collection("ngos").document(doc.id)
        doc_ref.update(ngo_data)

def get_ngo_data(db, email):
    """
    Fetch NGO data from Firestore using the provided email.
    :param db: Firestore client instance
    :param email: Email of the logged-in NGO
    :return: NGO data document
    """
    ngos_ref = db.collection("ngos").where("email", "==", email).limit(1)
    results = ngos_ref.stream()

    for doc in results:
        return doc.to_dict()
