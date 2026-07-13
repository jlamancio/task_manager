from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.usuario_db import UsuarioDB

SECRET_KEY = "chave-secreta-trocar-em-producao"
ALGORITHM = "HS256"
EXPIRACAO_MINUTOS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)


def criar_token(dados: dict, expires_delta: timedelta = None) -> str:
    payload = dados.copy()
    if expires_delta:
        expiracao = datetime.now(timezone.utc) + expires_delta
    else:
        expiracao = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACAO_MINUTOS)
    payload.update({"exp": expiracao})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def criar_usuario(email: str, senha: str, db: Session) -> UsuarioDB:
    senha_hashed = hash_senha(senha)
    usuario = UsuarioDB(email=email, senha_hash=senha_hashed)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def verificar_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
