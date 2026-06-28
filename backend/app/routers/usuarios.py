from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Usuario
from app.schemas import UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

# Rota: Listar todos os usuários da equipe do Ricardo
@router.get("/", response_model=List[UsuarioResponse], status_code=status.HTTP_200_OK)
def listar_usuarios(db: Session = Depends(get_db)):
    """
    Retorna a lista completa de colaboradores e administradores cadastrados.
    Utilizado pelo Frontend para exibir a equipe e vincular pessoas às tarefas.
    """
    try:
        usuarios = db.query(Usuario).all()
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar usuários: {str(e)}"
        )