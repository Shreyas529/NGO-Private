from Firebase.db_interaction import NGO_Database
from Firebase.cred import initialize_firebase
import unittest
from Firebase.authenticate import authenticate_ngo, create_user
import time
class Test_Database(unittest.TestCase):
    
    def setUp(self):
        self.db = initialize_firebase()
        self.ngo_db = NGO_Database(self.db)
        email = "test@gmail.com"
        password = "password"

        create_user(email, password)
        self.id_token = authenticate_ngo(email, password)

    
    def test_add_NGO(self):

        # Test adding NGO
        ngo_name = "Test NGO"
        description = "Test description"
        email = "test@gmail.com"
        needs = "food,clothes,books"
        image_logo = None
        phone = "1234567890"
        metamask_address = "0x1234567890"
        category = "General"

        self.ngo_db.add_NGO(self.id_token, ngo_name, category, image_logo, description, phone, needs, email, metamask_address)
        time.sleep(2)
        ngos=self.ngo_db.get_ngo(ngo_name)
        self.assertIsNotNone(ngos)
        
        self.assertEqual(ngos["Name"], ngo_name)
        self.assertEqual(ngos["Description"], description)
        self.assertEqual(ngos["email"], email)
        self.assertEqual(ngos["Phone"], phone)
        self.assertEqual(ngos["metamask_address"], metamask_address)
        self.assertIn("food", ngos["needs"])
        self.assertIn("clothes", ngos["needs"])
        self.assertIn("books", ngos["needs"])
        

    def test_update_NGO_needs(self):
        
        try:
            self.ngo_db.update_NGO_Needs(self.id_token, "Test NGO", "clothes, books")
        except:
            email = "test@gmail.com"
            password = "password"
            self.id_token = authenticate_ngo(email, password)
            time.sleep(1)
            self.ngo_db.update_NGO_Needs(self.id_token, "Test NGO", "clothes, books")


        time.sleep(2)
        ngos=self.ngo_db.get_ngo("Test NGO")
        self.assertIsNotNone(ngos)

        self.assertIn("clothes", ngos["needs"])
        self.assertIn("books", ngos["needs"])
        self.assertNotIn("food", ngos["needs"])
    
    def test_update_NGO_description(self):
        
        try:
            self.ngo_db.update_NGO_Description(self.id_token, "Test NGO", "New description")
        except:
            email = "test@gmail.com"
            password = "password"
            self.id_token = authenticate_ngo(email, password)
            time.sleep(1)
            self.ngo_db.update_NGO_Description(self.id_token, "Test NGO", "New description")

        time.sleep(3)
        ngo=self.ngo_db.get_ngo("Test NGO")
        self.assertIsNotNone(ngo)

        self.assertEqual(ngo["Description"], "New description")
        self.assertNotEqual(ngo["Description"], "Test description")
    
    def test_update_NGO_phone(self):
        
        try:
            self.ngo_db.update_NGO_Phone(self.id_token, "Test NGO", "0987654321")
        except:
            email = "test@gmail.com"
            password = "password"
            self.id_token = authenticate_ngo(email, password)
            time.sleep(1)
            self.ngo_db.update_NGO_Phone(self.id_token, "Test NGO", "0987654321")
        time.sleep(2)

        ngo=self.ngo_db.get_ngo("Test NGO")
        self.assertIsNotNone(ngo)

        self.assertEqual(ngo["Phone"], "0987654321")
        self.assertNotEqual(ngo["Phone"], "1234567890")
    
    def test_update_NGO_category(self):
        
        try:
            self.ngo_db.update_NGO_Category(self.id_token, "Test NGO", "Old Age Home")
        except:
            email = "test@gmail.com"
            password = "password"
            self.id_token = authenticate_ngo(email, password)
            time.sleep(1)
            self.ngo_db.update_NGO_Category(self.id_token, "Test NGO", "Old Age Home")
        time.sleep(2)

        ngo=self.ngo_db.get_ngo("Test NGO")
        self.assertIsNotNone(ngo)

        self.assertEqual(ngo["Category"], "Old Age Home")
        self.assertNotEqual(ngo["Category"], "General")

def clean_up_test_data():
    db = initialize_firebase()
    ngo_db = NGO_Database(db)
    ngo_db.delete_ngo("Test NGO")

if __name__ == "__main__":
    
    unittest.main()
    clean_up_test_data()