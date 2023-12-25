#!/usr/bin/env python3
from jwt import JWT, jwk_from_pem
import time
import sys
import os

# Get PEM file path
pem = os.path.join(os.path.dirname(__file__), "private-key.pem")

# Get the App ID
app_id = int(os.environ.get("APP_ID")) 

# Open PEM
with open(pem, 'rb') as pem_file:
    signing_key = jwk_from_pem(pem_file.read())

payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600,
    # GitHub App's identifier
    'iss': app_id
}

# Create JWT
jwt_instance = JWT()
encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

print(f"JWT:  {encoded_jwt}")
