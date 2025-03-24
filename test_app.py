import sys
import os
import unittest
import datetime

# Add the parent directory to the path to import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app  # Now we can import app.py

class JWKSAppTest(unittest.TestCase):
    def setUp(self):
        # Initialize the database and add test keys
        app.init_db()
        
        # Insert an expired key and a valid key for testing
        expired_time = int((datetime.datetime.now() - datetime.timedelta(hours=1)).timestamp())
        valid_time = int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
        
        # Save both keys in the database for testing purposes
        app.save_key(app.generate_private_key(), expired_time)
        app.save_key(app.generate_private_key(), valid_time)

    def test_auth_unexpired_key(self):
        # Test the /auth endpoint to get a valid token with a non-expired key
        with app.app.test_client() as client:
            response = client.post('/auth')
            self.assertEqual(response.status_code, 200)
            self.assertIn('token', response.json)
            # Additional check to ensure token structure (optional)
            self.assertTrue(isinstance(response.json['token'], str))

    def test_auth_expired_key(self):
        # Test the /auth endpoint to get a token with an expired key
        with app.app.test_client() as client:
            response = client.post('/auth?expired=true')
            self.assertEqual(response.status_code, 200)
            self.assertIn('token', response.json)
            # Check that a token is returned even for expired requests (optional)
            self.assertTrue(isinstance(response.json['token'], str))

    def test_no_keys_in_database(self):
        # Clear keys from the database and test that /auth returns 404 when no key is available
        with app.get_db() as conn:
            conn.execute("DELETE FROM keys")
        with app.app.test_client() as client:
            response = client.post('/auth')
            self.assertEqual(response.status_code, 404)

    def test_jwks_route(self):
        # Test the /.well-known/jwks.json endpoint to ensure valid keys are returned
        with app.app.test_client() as client:
            response = client.get('/.well-known/jwks.json')
            self.assertEqual(response.status_code, 200)
            self.assertIn("keys", response.json)
            # Verify that keys are present in the JWKS response
            self.assertTrue(len(response.json["keys"]) > 0)
            # Optional: Check the structure of the returned JWKs
            for key in response.json["keys"]:
                self.assertIn("kid", key)
                self.assertIn("kty", key)
                self.assertIn("use", key)
                self.assertIn("alg", key)
                self.assertIn("n", key)
                self.assertIn("e", key)

if __name__ == '__main__':
    unittest.main()