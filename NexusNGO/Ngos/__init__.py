# Ngos/__init__.py

# Import the necessary modules from the Ngos package
from .register_ngo import ngo_registration
from .ngo_interface import ngo_interface

# Define what gets imported when * is used
__all__ = ["ngo_registration", "ngo_interface"]
