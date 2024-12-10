import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import base64
from blockchain.blockchain import get_transactions_last_3_minutes
from Image_Detection.image_to_text import Response, encode_image
import os



class TestGetTransactionsLast3Minutes(unittest.TestCase):
    
    def test_get_transactions_last_3_minutes(self,):
        public_keys = ['0x8362F6588682a8DDf898026B792B804AE7719895']
        with patch('pandas.DataFrame.to_csv', return_value=None) as mock_to_csv:
            result = get_transactions_last_3_minutes(public_keys)

        # Verify results
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('blockNumber', result.columns)
        self.assertIn('from', result.columns)
        self.assertIn('to', result.columns)
        self.assertIn('value', result.columns)
        self.assertIn('hash', result.columns)
        self.assertIn('gas', result.columns)
        self.assertIn('gasPrice', result.columns)
        self.assertIn('input', result.columns)
        self.assertIn('timestamp', result.columns)

        # Check if the DataFrame was saved to CSV
        mock_to_csv.assert_called_once_with('transactions.csv', index=False)

class TestResponseClass(unittest.TestCase):

    def test_handle_image(self,):
        
        encoded_image = encode_image("Testing/test_image.jpg")
        response = Response(type="image", content=encoded_image)

        # Assert the _handle_image method was called and response was handled correctly
        objects=[i.lower().strip() for i in response.objects]
        
        self.assertTrue(any(["shirt" in i  for i in objects]))
 

    
   
    def test_handle_text(self,):
    
        response = Response(type="text", content="I want to donate a shirt and a pant")
        
        # Assert the _handle_text method processed the response correctly
        objects=[i.lower().strip() for i in response.objects]
        self.assertTrue(any(["shirt" in i  for i in objects]))
        self.assertTrue(any(["pant" in i  for i in objects]))

    def test_encode_image(self):
        # Create a temporary image file for testing
        test_image_path = "test_image.jpg"
        with open(test_image_path, "wb") as img_file:
            img_file.write(b"fake_image_data")

        # Test encoding the image
        encoded_image = encode_image(test_image_path)
        expected_encoding = base64.b64encode(b"fake_image_data").decode("utf-8")
        
        # Assert the encoding is correct
        self.assertEqual(encoded_image, expected_encoding)
        
        os.remove(test_image_path)



        
if __name__ == '__main__':
    unittest.main()
