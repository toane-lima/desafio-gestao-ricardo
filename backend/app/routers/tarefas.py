from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Tarefa
from app.schemas import TarefaResponse, TarefaCreate

# 1. Cria o roteador específico para as demandas
router = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"]
)

# 2. Rota: Listagem Geral (Alimenta as colunas do Quadro Kanban)
@router.get("/", response_model=List[TarefaResponse], status_code=status.HTTP_200_OK)
def listar_tarefas(db: Session = Depends(get_db)):
    """
    Retorna todas as tarefas cadastradas no banco de dados.
    O Frontend usará o campo 'status' de cada item para distribuí-los
    nas colunas (A Fazer, Em Andamento, Bloqueado, Concluído) do Kanban.
    """
    try:
        tarefas = db.query(Tarefa).all()
        return tarefas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao buscar as tarefas: {str(e)}"
        )

from sqlalchemy import text
from app.schemas import DashboardMetricas, TaxaEntregaPrazo, SemaforoPrazoResponse, SemaforoCapacidadeResponse

# ==========================================
# 3. Rota: Métricas Gerais do Dashboard (KPIs)
# ==========================================
@router.get("/dashboard/metricas", response_model=DashboardMetricas, status_code=status.HTTP_200_OK)
def obter_metricas_dashboard(db: Session = Depends(get_db)):
    """
    Calcula os números absolutos de tarefas por status e o total de vencidas.
    Alimenta os contadores principais do topo da tela do Ricardo.
    """
    try:
        query = text("""
            SELECT 
                COUNT(*) as total_tarefas,
                COUNT(CASE WHEN status = 'done' THEN 1 END) as concluidas,
                COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as em_andamento,
                COUNT(CASE WHEN status = 'blocked' THEN 1 END) as bloqueadas,
                COUNT(CASE WHEN status = 'todo' THEN 1 END) as a_fazer,
                COUNT(CASE WHEN status != 'done' AND data_entrega < CURRENT_DATE THEN 1 END) as vencidas
            FROM gestao.tarefas;
        """)
        resultado = db.execute(query).fetchone()
        
        return DashboardMetricas(
            total_tarefas=resultado.total_tarefas,
            concluidas=resultado.concluidas,
            em_andamento=resultado.em_andamento,
            bloqueadas=resultado.bloqueadas,
            a_fazer=resultado.a_fazer,
            vencidas=resultado.vencidas
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular métricas: {str(e)}")


# ==========================================
# 4. Rota: Taxa de Entrega no Prazo (Gráfico de Pizza)
# ==========================================
@router.get("/dashboard/taxa-prazo", response_model=TaxaEntregaPrazo, status_code=status.HTTP_200_OK)
def obter_taxa_entrega_prazo(db: Session = Depends(get_db)):
    """
    Compara tarefas concluídas dentro do prazo estipulado vs fora do prazo.
    Gera a porcentagem exata para desenhar o gráfico de pizza de eficiência.
    """
    try:
        query = text("""
            SELECT 
                COUNT(CASE WHEN data_conclusao <= data_entrega THEN 1 END) as no_prazo,
                COUNT(CASE WHEN data_conclusao > data_entrega THEN 1 END) as fora_do_prazo
            FROM gestao.tarefas
            WHERE status = 'done';
        """)
        resultado = db.execute(query).fetchone()
        
        total = resultado.no_prazo + resultado.fora_do_prazo
        porcentagem = (resultado.no_prazo / total * 100) if total > 0 else 0.0
        
        return TaxaEntregaPrazo(
            no_prazo=resultado.no_prazo,
            fora_do_prazo=resultado.fora_do_prazo,
            porcentagem_no_prazo=round(porcentagem, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular taxa de prazo: {str(e)}")


# ==========================================
# 5. Rota: Semáforo de Prazos das Demandas Ativas
# ==========================================
@router.get("/semaforos/prazos", response_model=List[SemaforoPrazoResponse], status_code=status.HTTP_200_OK)
def obter_semaforo_prazos(db: Session = Depends(get_db)):
    """
    Retorna os dias restantes para cada tarefa ativa e a classificação de risco:
    - Crítico (Vermelho): <= 2 dias ou Vencida
    - Atenção (Amarelo): 3 a 5 dias
    - Normal (Verde): > 5 dias
    """
    try:
        query = text("""
            SELECT 
                titulo,
                nome_cliente,
                data_entrega,
                (data_entrega - CURRENT_DATE) as dias_restantes,
                CASE 
                    WHEN (data_entrega - CURRENT_DATE) <= 2 THEN 'Vermelho'
                    WHEN (data_entrega - CURRENT_DATE) BETWEEN 3 AND 5 THEN 'Amarelo'
                    ELSE 'Verde'
                END as semaforo_prazo
            FROM gestao.tarefas
            WHERE status != 'done'
            ORDER BY dias_restantes ASC;
        """)
        resultados = db.execute(query).fetchall()
        
        return [
            SemaforoPrazoResponse(
                titulo=row.titulo,
                nome_cliente=row.nome_cliente,
                data_entrega=row.data_entrega,
                dias_restantes=row.dias_restantes,
                semaforo_prazo=row.semaforo_prazo
            ) for row in resultados
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar semáforo de prazos: {str(e)}")


# ==========================================
# 6. Rota: Semáforo de Capacidade Operacional do Time
# ==========================================
@router.get("/semaforos/capacidade", response_model=List[SemaforoCapacidadeResponse], status_code=status.HTTP_200_OK)
def obter_semaforo_capacidade(db: Session = Depends(get_db)):
    """
    Mapeia a sobrecarga de trabalho de cada colaborador da equipe do Ricardo:
    - Sobrecarregado (Vermelho): > 3 tarefas simultâneas em andamento
    - No Limite (Amarelo): 2 ou 3 tarefas
    - Confortável (Verde): 0 ou 1 tarefa
    """
    try:
        query = text("""
            SELECT 
                u.nome as colaborador,
                COUNT(tc.tarefa_id) as tarefas_ativas,
                CASE 
                    WHEN COUNT(tc.tarefa_id) > 3 THEN 'Vermelho'
                    WHEN COUNT(tc.tarefa_id) BETWEEN 2 AND 3 THEN 'Amarelo'
                    ELSE 'Verde'
                END as semaforo_capacidade
            FROM gestao.usuarios u
            LEFT JOIN gestao.tarefa_colaboradores tc ON u.id = tc.colaborador_id
            LEFT JOIN gestao.tarefas t ON tc.tarefa_id = t.id AND t.status IN ('todo', 'in_progress', 'blocked')
            GROUP BY u.id, u.nome
            ORDER BY tarefas_ativas DESC;
        """)
        resultados = db.execute(query).fetchall()
        
        return [
            SemaforoCapacidadeResponse(
                colaborador=row.colaborador,
                tarefas_ativas=row.tarefas_ativas,
                semaforo_capacidade=row.semaforo_capacidade
            ) for row in resultados
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar semáforo de capacidade: {str(e)}")