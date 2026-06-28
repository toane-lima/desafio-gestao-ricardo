from sqlalchemy import Column, String, Text, Date, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

# 1. Tabela Intermediária para o relacionamento Muitos-para-Muitos (Cooperação de Tarefas)
# Como ela serve apenas para ligar as chaves, podemos usar o construtor Table do SQLAlchemy
tarefa_colaboradores = Table(
    "tarefa_colaboradores",
    Base.metadata,
    Column("tarefa_id", UUID(as_uuid=True), ForeignKey("gestao.tarefas.id", ondelete="CASCADE"), primary_key=True),
    Column("colaborador_id", UUID(as_uuid=True), ForeignKey("gestao.usuarios.id", ondelete="CASCADE"), primary_key=True),
    schema="gestao"  # Garante que a tabela seja criada dentro do esquema correto
)


# 2. Modelo de Usuários
class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "gestao"}  # Aponta explicitamente para o esquema gestao

    # server_default=func.gen_random_uuid() avisa o SQLAlchemy que o banco gera o UUID sozinho
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    cargo = Column(String(50), nullable=False)
    perfil = Column(String(20), nullable=False)  # 'admin' ou 'colaborador'


# 3. Modelo de Tarefas (Demandas)
class Tarefa(Base):
    __tablename__ = "tarefas"
    __table_args__ = {"schema": "gestao"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    titulo = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    nome_cliente = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="todo")  # 'todo', 'in_progress', 'blocked', 'done'
    
    # server_default=func.current_date() faz o banco registrar o dia da criação automaticamente
    data_criacao = Column(Date, nullable=False, server_default=func.current_date())
    data_entrega = Column(Date, nullable=False)
    data_conclusao = Column(Date, nullable=True)