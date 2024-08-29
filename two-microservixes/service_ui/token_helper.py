from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
import jwt

api_key = APIKeyHeader(name="Authorization")


SECRET_KEY = """-----BEGIN PUBLIC KEY-----
                MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqtXUlS3ne6Ij1lem602JaYZHSzrpv/7nklgmgIxv/MH6KZkSRPP8pQXWvxqhXNpqwylsy/uI5ZFisTDib9PWD7aupTSgddmVfQmdTrTCUR1wu0Kr+7yhtESfPPfIlyUB5fuxWmoeiJLGEfsCq9NfXay2EBn5EPKyqElCRAVCBh1J4dlV0FTavRzOsnd+0BYp0UCnlvw346JmyW9gE8GgaOFlQhWWsQrAs/T/P8GTXLqrf4sBhPGpRyoU+MrAMrc5h9P1+TH7qBOphkJAMexRWTaBGu7knyKk7Ezf5XMPZxPKvf+MjBSaJtCdLFYPEhzHbyjy8wvXyvp2cVCFXUm7iQIDAQAB
                -----END PUBLIC KEY-----"""

def get_jwt_claims(authorization: str = Security(api_key)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized! Missing Authorization in Header')

    if not authorization.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized! Only Bearer Tokens are Supported')

    token_string = authorization[7:]
    #options = {"verify_signature": False, "require": ["exp", "iss", "sub", "iat", "tenant_name"]}
    options = {"verify_signature": False}

    try:
        token_headers = jwt.get_unverified_header(token_string)
        ret = jwt.decode(token_string, key=SECRET_KEY, algorithms=["HS256"], options=options)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return {"jwt_payload": ret}