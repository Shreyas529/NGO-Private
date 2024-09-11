import firebase_admin
from firebase_admin import credentials, firestore, auth

def initialize_firebase():
    """
    Initialize Firebase app and Firestore.
    :return: Firestore client instance
    """
    
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'colossus-726c5.appspot.com'
        })

    # Initialize Firestore
    db = firestore.client()
    return db
