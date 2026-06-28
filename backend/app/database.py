import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# 2. Puxa a string de conexão do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

# Segurança: Garante que o sistema não vai subir se o .env estiver errado ou ausente
if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não foi encontrada no arquivo .env")

# 3. Cria o "Engine" (O motor que gerencia a conexão física com o PostgreSQL)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Prática recomendada em MLOps: checa se a conexão está viva antes de usar
)

# 4. Cria a fábrica de sessões (SessionLocal). Cada requisição da API terá sua própria sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Cria a classe Base que todos os nossos modelos (models.py) vão herdar
Base = declarative_base()

# 6. Função utilitária (Dependency Injection) para abrir e fechar o banco automaticamente nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()