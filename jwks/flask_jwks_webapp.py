"""
Create a JWKS Endpoint
=======================
Use Flask to create a simple web server that serves the JWKS.
"""

from flask import Flask, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import json
import base64

app = Flask(__name__)

# Load the public key
with open('public_key.pem', 'rb') as f:
    public_pem = f.read()

# Convert public key to JWK format
public_key = serialization.load_pem_public_key(public_pem)
public_numbers = public_key.public_numbers()

# Base64 encode the key components
n = base64.urlsafe_b64encode(
    public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, byteorder='big')).decode('utf-8').rstrip('=')
e = base64.urlsafe_b64encode(
    public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, byteorder='big')).decode('utf-8').rstrip('=')

# Create the JWKS structure
jwks = {
    "keys": [
        {
            "kty": "RSA",
            "use": "sig",
            "kid": "my-key-id",
            "n": n,
            "e": e,
            "alg": "RS256"
        }
    ]
}


@app.route('/.well-known/jwks.json')
def jwks_endpoint():
    return jsonify(jwks)


if __name__ == '__main__':
    app.run(port=5001)
