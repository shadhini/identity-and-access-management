## Generate Public/Private Key Pair & Host a JWKS Endpoint

_[ using Python, the `cryptography` library and Flask ]_

---

**JSON Web Key Set** (`JWKS`): JSON data structure that represents a set of JSON Web Keys (`JWK`). 
* JWKS endpoints are commonly used in `OAuth 2.0` and `OpenID Connect` to expose a set of public keys.


#### Step 1: Install Required Libraries
```sh
source .venv/bin/activate
pip install cryptography flask pyjwt
```

#### Step 2: Generate Public/Private Key Pair

```sh
python3 gen_keys.py 
```

#### Step 3: Run Flask app to serve JWKS Endpoint

```sh
FLASK_APP=flask_jwks_webapp.py flask run --port=5001
```

#### Step 4: Test the JWKS Endpoint
Navigate to `http://localhost:5001/.well-known/jwks.json` to see the JWKS.

