Project 2 – Extending the JWKS Server

Overview:
This project enhances a JSON Web Key Set (JWKS) server by integrating a SQLite database for private key storage. It includes secure JWT issuance, query parameter use to prevent SQL injection, and support for serving public keys through a JWKS endpoint.

Features Implemented:
- /auth endpoint signs JWTs using a valid or expired private key from the database based on the request.
- /.well-known/jwks.json returns a JSON Web Key Set of all valid (non-expired) public keys.
- SQLite database (totally_not_my_privateKeys.db) is used to persist RSA private keys.
- SQL queries use parameterized statements to defend against SQL injection.
- RSA keys are serialized to PEM strings for storage and deserialized for signing.
- Passed all Gradebot tests: 65/65 points.
- Test suite (test_app.py) included with >80% test coverage.

Database Details:
- File: totally_not_my_privateKeys.db

Schema:
CREATE TABLE IF NOT EXISTS keys (
    kid INTEGER PRIMARY KEY AUTOINCREMENT,
    key BLOB NOT NULL,
    exp INTEGER NOT NULL
);

At least one expired and one valid key is stored at app start.

Endpoints:
POST /auth
- If 'expired' query parameter is present, uses an expired key.
- Otherwise, uses an unexpired key to sign and return a JWT.

GET /.well-known/jwks.json
- Returns all valid (non-expired) keys as a JWKS response.

Testing Instructions:
1. Run the server:
   python app.py

2. Run Gradebot:
   ./gradebot project2

3. Run tests:
   python -m unittest test_app.py

Files Included:
- app.py – Main application logic (Flask + SQLite + JWT)
- test_app.py – Unit tests with assertions for endpoints and JWTs
- gradebot.exe – Testing client used to verify correctness
- LICENSE – MIT license file
- Screenshot of Gradebot output (all 65 points)
- Screenshot of server running and handling /auth and /jwks.json requests

Requirements:
- Python 3.8+
- Flask
- PyJWT
- cryptography
- sqlite3 (Python standard library)

License:
This project is licensed under the MIT License. See the LICENSE file for full details.

Result:
The JWKS server is fully functional, secure against SQL injection, and supports persistent key storage with accurate JWT issuance. All automated tests and grading checks pass successfully.
