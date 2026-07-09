from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    return verificar_token(token)