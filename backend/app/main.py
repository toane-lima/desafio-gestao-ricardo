from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tarefas, usuarios

# 1. Inicializa a aplicação FastAPI com metadados para a documentação
app = FastAPI(
    title="Sistema de Gestão de Demandas - API",
    description="Backend em FastAPI para resolver o gargalo de gestão de tarefas e capacidade da equipe do Ricardo.",
    version="1.0.0"
)

# 2. Configuração do CORS (Crucial para o Frontend conseguir conversar com o Backend)
# Como o React/TypeScript vai rodar em uma porta diferente no futuro, precisamos liberar o acesso.
origins = [
    "http://localhost:3000",  # Porta padrão do React
    "http://localhost:5173",  # Porta padrão do Vite (se usarmos React moderno)
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos os cabeçalhos HTTP
)

# 3. Inclui os roteadores da nossa aplicação
app.include_router(tarefas.router)
app.include_router(usuarios.router)

# 4. Rota raiz de boas-vindas (Apenas para teste rápido no navegador)
@app.get("/", tags=["Raiz"])
def ler_raiz():
    return {
        "mensagem": "API de Gestão de Demandas rodando com sucesso!",
        "status": "Online",
        "documentacao": "/docs"
    }

