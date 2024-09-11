import firebase_admin
from firebase_admin import credentials, firestore, auth

def initialize_firebase():
    """
    Initialize Firebase app and Firestore.
    :return: Firestore client instance
    """
    # Check if the Firebase app is already initialized
    if not firebase_admin._apps:
        # Path to your Firebase service account key JSON file
        cred = credentials.Certificate("path/to/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

    # Initialize Firestore
    db = firestore.client()
    return db
