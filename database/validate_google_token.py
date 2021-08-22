import json
import jwt
import requests

def validate_security_token(token, client_ids):
    # Get Google's RISC configuration.
    risc_config_uri = 'https://accounts.google.com/.well-known/risc-configuration'
    risc_config = requests.get(risc_config_uri).json()

    # Get the public key used to sign the token.
    google_certs = requests.get(risc_config['jwks_uri']).json()

    jwt_header = jwt.get_unverified_header(token)

    key_id = jwt_header['kid']
    public_key = None
    for key in google_certs['keys']:
        if key['kid'] == key_id:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
    if not public_key:
        raise Exception('Public key certificate not found.')
        # In this situation, return HTTP 400

    # Decode the token, validating its signature, audience, and issuer.
    try:
        token_data = jwt.decode(token, public_key, algorithms='RS256',
                                # options={'verify_exp': False},)
                                audience=client_ids, issuer=risc_config['issuer'])
    except:
        raise
        # Validation failed. Return HTTP 400.
    return token_data