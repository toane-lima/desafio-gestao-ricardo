from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List
from uuid import UUID

# ==========================================
# SCHEMAS DE USUÁRIO (COLABORADORES)
# ==========================================

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    cargo: str
    perfil: str  # 'admin' ou 'colaborador'

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: UUID

    class Config:
        from_attributes = True


# ==========================================
# SCHEMAS DE TAREFA (DEMANDAS)
# ==========================================

class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    nome_cliente: str
    status: str = "todo"  # 'todo', 'in_progress', 'blocked', 'done'
    data_entrega: date

class TarefaCreate(TarefaBase):
    pass

class TarefaResponse(TarefaBase):
    id: UUID
    data_criacao: date
    data_conclusao: Optional[date] = None

    class Config:
        from_attributes = True


# ==========================================
# SCHEMAS ESPECÍFICOS PARA OS KPIs E SEMÁFOROS
# ==========================================

class DashboardMetricas(BaseModel):
    total_tarefas: int
    concluidas: int
    em_andamento: int
    bloqueadas: int
    a_fazer: int
    vencidas: int

class TaxaEntregaPrazo(BaseModel):
    no_prazo: int
    fora_do_prazo: int
    porcentagem_no_prazo: float

class SemaforoPrazoResponse(BaseModel):
    titulo: str
    nome_cliente: str
    data_entrega: date
    dias_restantes: int
    semaforo_prazo: str

class SemaforoCapacidadeResponse(BaseModel):
    colaborador: str
    tarefas_ativas: int
    semaforo_capacidade: str