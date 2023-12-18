from fastapi import HTTPException,status
from jose import jwt,JWTError
import requests 
import os 
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()


KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT = os.getenv("KEYCLOAK_CLIENT")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_ADMIN = os.getenv("KEYCLOAK_ADMIN")
KEYCLOAK_ADMIN_EMAIL = os.getenv("KEYCLOAK_ADMIN_EMAIL")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
AUDIENCE = os.getenv("AUDIENCE")
ALGORITHM = os.getenv("ALGORITHM")


def login_keycloak_user(email,password):
    keycloak_login_data = {
        'grant_type': 'password',
        'client_id': KEYCLOAK_CLIENT,
        'client_secret': KEYCLOAK_CLIENT_SECRET,
        'username': email,
        'password': password,
    }
    url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    try:
        response = requests.post(url, data=keycloak_login_data)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")

admin_token = login_keycloak_user(KEYCLOAK_ADMIN_EMAIL, KEYCLOAK_ADMIN_PASSWORD)
access_token_expire_date = datetime.now() + timedelta(seconds=admin_token.get('expires_in'))
refresh_token_expire_date = datetime.now() + timedelta(seconds=admin_token.get('refresh_expires_in'))

def refresh_user_token():
    keycloak_login_data = {
        'grant_type': 'refresh_token',
        'client_id': KEYCLOAK_CLIENT,
        'client_secret': KEYCLOAK_CLIENT_SECRET,
        'refresh_token': admin_token.get('refresh_token'),
    }
    url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    try:
        response = requests.post(url, data=keycloak_login_data)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")




def refresh_or_get_new_admin_token():
    global admin_token, access_token_expire_date,refresh_token_expire_date
    if datetime.now() > access_token_expire_date:
        if datetime.now() > refresh_token_expire_date:
            admin_token = login_keycloak_user(KEYCLOAK_ADMIN_EMAIL, KEYCLOAK_ADMIN_PASSWORD)
            access_token_expire_date = datetime.now() + timedelta(seconds=admin_token.get('expires_in'))
            refresh_token_expire_date = datetime.now() + timedelta(seconds=admin_token.get('refresh_expires_in'))
        else:
            admin_token = refresh_user_token()
            access_token_expire_date = datetime.now() + timedelta(seconds=admin_token.get('expires_in'))
            refresh_token_expire_date = datetime.now() + timedelta(seconds=admin_token.get('refresh_expires_in'))
    return admin_token

def register_keycloak_user(user_data,db_id):
    keycloak_register_data = {
        "username": user_data.first_name[0] + user_data.last_name,
        "firstName": user_data.first_name,
        "lastName": user_data.last_name,
        "email": user_data.email,
        "enabled": True,
        "credentials": [
            {
                "type": "password",
                "value": user_data.password,
                "temporary": False
            }
        ],
        "attributes": {
            "db_id": str(db_id)  
        }
    }
    
    admin_token = refresh_or_get_new_admin_token()
    headers = {
        "Authorization": f"Bearer {admin_token.get('access_token')}",
        "Content-Type": "application/json"
    }
    url = f"{KEYCLOAK_URL}/admin/realms/{KEYCLOAK_REALM}/users"
    try:
        response = requests.post(url, json=keycloak_register_data, headers=headers)
        return response.status_code
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    
    
    
    
DECODE_KEY= "-----BEGIN PUBLIC KEY-----\n" + PUBLIC_KEY + "\n-----END PUBLIC KEY-----"
def verify_token(token):
    try:
        payload = jwt.decode(token, key=DECODE_KEY, audience=AUDIENCE, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    
