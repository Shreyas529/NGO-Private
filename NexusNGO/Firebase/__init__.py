# Firebase/__init__.py

# Import necessary modules for easy access
from .firebase_config import initialize_firebase
from .db_interaction import (
    register_ngo,
    authenticate_ngo,
    get_top_ngos,
    search_ngos_by_items,
    update_ngo_profile,
    get_ngo_data
)

# Define what gets imported when * is used
__all__ = [
    "initialize_firebase",
    "register_ngo",
    "authenticate_ngo",
    "get_top_ngos",
    "search_ngos_by_items",
    "update_ngo_profile",
    "get_ngo_data"
]
