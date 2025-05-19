import numpy as np
import bentoml
from bentoml.io import NumpyNdarray, JSON
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from datetime import datetime, timedelta

# Secret key et algorithme pour JWT authentication
JWT_SECRET_KEY = "eef9b82726018d6aa569f60bb0e136c5de3a3441a8713bfbce1c85464c930ea9ed4bbe18dd7cf202bbdec06f098716ec470bfd33674e755deedfc4c39da445954d8e81587dc5b17011d098cb1b1599d39d13f28ab3593cafe6e4c9c366548f3d9320560a9c93fb5e9a31b5233ce9b592ef6b797e29ba7f15d46a6a40dfc477f3ce2519abec14a4d888df79dccf10ee956d7eddfbe0ff77cf7921e06aefce18d657f0a33dad31a95ecaf9d62c7e8e64f8bb741dbb5a510a782057969ece9575f9cc96863ec2298ce78ed4e559f0c37f06365658d12123ed3e636c90969172bee8d04a27508ef27efddf0d5c3c51e8879307cb8a795b793319a326221d26348249"
JWT_ALGORITHM = "HS256"

# Compte pour l'authentification
USERS = {
    "admin": "admin123",
}

# Création d'un middleware pour la partie sécurisation
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/v1/models/admission/predict":
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})

            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            request.state.user = payload.get("sub")

        response = await call_next(request)
        return response

# Pydantic model pour valider les données enentrées
class InputModel(BaseModel):
    grescore: int
    toeflScore: int
    universityrating: int
    sop: float
    lor: float
    cgpa: float
    research: int

# Récupération du modèle
admission_lr_runner = bentoml.sklearn.get("admission_lr:latest").to_runner()

# Création du service api
lr_service = bentoml.Service("lr_service", runners=[admission_lr_runner])

# Ajout du middleware pour l'uathentification
lr_service.add_asgi_middleware(JWTAuthMiddleware)

# Création du endpoint
@lr_service.api(input=JSON(), output=JSON())
def login(credentials: dict) -> dict:
    username = credentials.get("username")
    password = credentials.get("password")

    if username in USERS and USERS[username] == password:
        token = create_jwt_token(username)
        return {"token": token}
    else:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

# Create an API endpoint for the service
@lr_service.api(
    input=JSON(pydantic_model=InputModel),
    output=JSON(),
    route='v1/models/admission/predict'
)
async def predict_admission(input_data: InputModel, ctx: bentoml.Context) -> dict:
    request = ctx.request
    user = request.state.user if hasattr(request.state, 'user') else None

    # Convert the input data to a numpy array
    input_series = np.array([input_data.grescore, input_data.toeflScore, input_data.universityrating, input_data.sop, input_data.lor, input_data.cgpa, input_data.research])

    result = await admission_lr_runner.predict.async_run(input_series.reshape(1, -1))

    return {
        "prediction": result.tolist(),
        "user": user
    }

# Function to create a JWT token
def create_jwt_token(user_id: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token