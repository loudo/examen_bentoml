import requests

# Paramètres
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/v1/models/admission/predict"

# Données de connexion
credentials_ok = {
    "username": "admin",
    "password": "admin123"
}

# Appel du service de connexion
def login_service(credentials):

    # Demande de connexion
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=credentials
    )

    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        response = { 'return_code': login_response.status_code, 'token': token }
    else:
        response = { 'return_code': login_response.status_code, 'token': -1 }

    return response


resp = login_service(credentials_ok)

print(resp['token'])