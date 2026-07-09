
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.usuario import UsuarioCreate, UsuarioResponse
from app.models.usuario_db import UsuarioDB
from app.services.auth_service import criar_usuario, verificar_senha, criar_token
from database.db import get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/cadastro", response_model=UsuarioResponse)
def cadastrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioDB).filter(
        UsuarioDB.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    return criar_usuario(usuario.email, usuario.senha, db)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_usuario = db.query(UsuarioDB).filter(
        UsuarioDB.email == form_data.username
    ).first()

    if not db_usuario or not verificar_senha(form_data.password, db_usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    
    token = criar_token({"sub": db_usuario.email})
    return {"access_token": token, "token_type": "bearer"}