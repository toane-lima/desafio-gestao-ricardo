export interface Usuario {
  id: string;
  nome: string;
  email: string;
  cargo: string;
  perfil: string;
}

export interface Tarefa {
  id: string;
  titulo: string;
  descricao?: string;
  status: 'todo' | 'in_progress' | 'blocked' | 'done';
  prioridade: 'Low' | 'Medium' | 'High';
  nome_cliente: string;
  data_entrega: string;
  data_conclusao?: string;
  colaboradores: Usuario[];
}

export interface DashboardMetricas {
  total_tarefas: number;
  concluidas: number;
  em_andamento: number;
  bloqueadas: number;
  a_fazer: number;
  vencidas: number;
}

export interface SemaforoPrazo {
  titulo: string;
  nome_cliente: string;
  data_entrega: string;
  dias_restantes: number;
  semaforo_prazo: 'Vermelho' | 'Amarelo' | 'Verde';
}

export interface SemaforoCapacidade {
  colaborador: string;
  tarefas_ativas: number;
  semaforo_capacidade: 'Vermelho' | 'Amarelo' | 'Verde';
}