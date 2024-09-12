import Firebase.authenticate as auth
import Firebase.db_interaction as db
import Firebase.cred as config
from Image_Detection.image_to_text import encode_image

database = config.initialize_firebase()



# sample_db = db.Database()

token = (auth.authenticate_ngo("U@gmail.com", "lmaolol@204"))

encoded_image = encode_image("/home/shreyasarun/Documents/Hackathons/Collosus/NGO-Private/NexusNGO/Screenshot from 2024-05-08 18-14-12.png")
db.NGO_Database(database).add_NGO(token, "Delhi", "Education", encoded_image, "description", "phone")