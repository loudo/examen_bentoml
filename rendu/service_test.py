import requests

# Paramètres
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/v1/models/admission/predict"

# Données de connexion
credentials_ok = {
    "username": "admin",
    "password": "admin123"
}

credentials_ko = {
    "username": "admin",
    "password": "admin"
}

# Données à envoyer au service
data_ok = {
    "grescore": 317,
    "toeflScore": 107,
    "universityrating": 2,
    "sop": 4.5,
    "lor": 8,
    "cgpa": 9.10,
    "research": 1
}

# Données à envoyer au service (ko)
data_ko = {
    "grescore": 317,
    "toeflScore": 107,
    "universityrating": 2,
    "sop": 4.5,
}

# Token Expire
expire_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0NzY3NTA1M30.XHzgRPxThRF1UfspTQWMS0uRTnm4bBxR2FtJ92Pu4Cw"

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

# Appel du service de prédiction
def predict_service(token, data):

    # Send a POST request to the prediction
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=data
    )

    return response

# Appel du service de prédiction sans autorization
def predict_service_without_auth(data):

    # Send a POST request to the prediction
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json"
        },
        json=data
    )

    return response

# Connexion OK
def test_login():
    response = login_service(credentials_ok)
    assert(response['token'] != -1)

# Connexion KO (Mauvaise crédiential)
def test_login_ko():
    response = login_service(credentials_ko)
    assert(response['return_code'] == 500)


# Predict OK
def test_predict_service():

    resp_login = login_service(credentials_ok)

    print(resp_login['token'])

    resp_predict = predict_service(resp_login['token'], data_ok)

    assert(resp_predict.status_code == 200)

# Predict KO
def test_predict_service_data_ko():

    resp_login = login_service(credentials_ok)

    resp_predict = predict_service(resp_login['token'], data_ko)

    assert(resp_predict.status_code == 400)

# Predict jwt KO
def test_predict_service_jwt_ko():

    resp_predict = predict_service("4564646", data_ok)

    assert(resp_predict.status_code == 401)

# Predict without auth
def test_predict_service_without_auth():

    resp_predict = predict_service_without_auth(data_ok)

    assert(resp_predict.status_code == 401)

# Predict with expire token
def test_predict_service_with_expire_token():

    resp_predict = predict_service(expire_token, data_ok)

    assert(resp_predict.status_code == 401)

    