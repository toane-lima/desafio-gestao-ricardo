import { useState, useEffect } from 'react';
import api from './api';
import type { DashboardMetricas, SemaforoPrazo, SemaforoCapacidade, Tarefa } from './types';

export default function App() {
  // Estados para os dados da API
  const [metricas, setMetricas] = useState<DashboardMetricas | null>(null);
  const [prazos, setPrazos] = useState<SemaforoPrazo[]>([]);
  const [capacidades, setCapacidades] = useState<SemaforoCapacidade[]>([]);
  const [tarefas, setTarefas] = useState<Tarefa[]>([]);
  const [carregando, setCarregando] = useState(true);

  // Carrega todos os dados do sistema em paralelo
  useEffect(() => {
    Promise.all([
      api.get('/tarefas/dashboard/metricas'),
      api.get('/tarefas/semaforos/prazos'),
      api.get('/tarefas/semaforos/capacidade'),
      api.get('/tarefas')
    ])
      .then(([resMetricas, resPrazos, resCapacidades, resTarefas]) => {
        setMetricas(resMetricas.data);
        setPrazos(resPrazos.data);
        setCapacidades(resCapacidades.data);
        setTarefas(resTarefas.data);
        setCarregando(false);
      })
      .catch((error) => {
        console.error("Erro ao carregar dados do painel:", error);
        setCarregando(false);
      });
  }, []);

  // Função auxiliar para renderizar as badges de cores do semáforo nas tabelas
  const renderBadgeCor = (cor: 'Vermelho' | 'Amarelo' | 'Verde') => {
    const estilos = {
      Vermelho: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
      Amarelo: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
      Verde: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
    };
    return (
      <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${estilos[cor]}`}>
        {cor}
      </span>
    );
  };

  // Definição das colunas do Kanban
  const colunas = [
    { id: 'todo', titulo: '📌 A Fazer', corBorda: 'border-t-slate-400', bgBadge: 'bg-slate-700/50' },
    { id: 'in_progress', titulo: '⚡ Em Andamento', corBorda: 'border-t-amber-500', bgBadge: 'bg-amber-500/20 text-amber-400' },
    { id: 'blocked', titulo: '🛑 Bloqueado', corBorda: 'border-t-rose-500', bgBadge: 'bg-rose-500/20 text-rose-400' },
    { id: 'done', titulo: '✅ Concluído', corBorda: 'border-t-emerald-500', bgBadge: 'bg-emerald-500/20 text-emerald-400' },
  ];

  // Função auxiliar para formatar a prioridade do cartão do Kanban
  const renderBadgePrioridade = (prioridade: 'Low' | 'Medium' | 'High') => {
    const estilos = {
      Low: 'bg-slate-700 text-slate-300',
      Medium: 'bg-blue-600/30 text-blue-400 border-blue-500/30',
      High: 'bg-rose-600/30 text-rose-400 border-rose-500/30'
    };
    return (
      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${estilos[prioridade]}`}>
        {prioridade}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 shadow-md">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              📊 Sistema de Gestão de Demandas
            </h1>
            <p className="text-sm text-slate-400 mt-0.5">
              Operação de Alto Desempenho • Painel de Controle do Ricardo
            </p>
          </div>
          <div className="flex items-center gap-3 bg-slate-900/50 px-4 py-2 rounded-lg border border-slate-700">
            <div className={`w-2.5 h-2.5 rounded-full ${carregando ? 'bg-amber-500 animate-pulse' : 'bg-emerald-500 animate-pulse'}`}></div>
            <span className="text-xs font-medium text-slate-300 uppercase tracking-wider">
              {carregando ? 'Sincronizando Banco...' : 'API Backend Conectada'}
            </span>
          </div>
        </div>
      </header>

      {/* Conteúdo Principal */}
      <main className="max-w-7xl mx-auto p-6 space-y-8">
        
        {/* KPIs do Topo */}
        <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-sm border-l-4 border-l-slate-500">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total de Demandas</p>
            <p className="text-3xl font-black mt-1 text-white">{carregando ? '...' : metricas?.total_tarefas}</p>
          </div>
          <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-sm border-l-4 border-l-amber-500">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Em Andamento</p>
            <p className="text-3xl font-black mt-1 text-amber-400">{carregando ? '...' : metricas?.em_andamento}</p>
          </div>
          <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-sm border-l-4 border-l-emerald-500">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Concluídas</p>
            <p className="text-3xl font-black mt-1 text-emerald-400">{carregando ? '...' : metricas?.concluidas}</p>
          </div>
          <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-sm border-l-4 border-l-rose-500">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Atrasadas / Críticas</p>
            <p className="text-3xl font-black mt-1 text-rose-400">{carregando ? '...' : metricas?.vencidas}</p>
          </div>
        </section>

        {/* Painel Operacional de Riscos (Semáforos) */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* Tabela 1: Semáforo de Prazos */}
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-md">
            <h2 className="text-lg font-bold text-white mb-1 flex items-center gap-2">
              ⏳ Alerta de Prazos por Demanda
            </h2>
            <p className="text-xs text-slate-400 mb-4">Gargalos críticos calculados dinamicamente com base no vencimento</p>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-700 text-slate-400 text-xs uppercase font-bold">
                    <th className="pb-3">Tarefa</th>
                    <th className="pb-3">Cliente</th>
                    <th className="pb-3">Dias Restantes</th>
                    <th className="pb-3 text-right">Status de Risco</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/50 text-sm">
                  {prazos.map((item, index) => (
                    <tr key={index} className="hover:bg-slate-700/30 transition-colors">
                      <td className="py-3 font-medium text-slate-200">{item.titulo}</td>
                      <td className="py-3 text-slate-400">{item.nome_cliente}</td>
                      <td className="py-3 text-slate-300">{item.dias_restantes} dias</td>
                      <td className="py-3 text-right">{renderBadgeCor(item.semaforo_prazo)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Tabela 2: Semáforo de Capacidade */}
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-md">
            <h2 className="text-lg font-bold text-white mb-1 flex items-center gap-2">
              👥 Capacidade Operacional do Time
            </h2>
            <p className="text-xs text-slate-400 mb-4">Mapeamento de sobrecarga baseado em tarefas simultâneas ativas</p>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-700 text-slate-400 text-xs uppercase font-bold">
                    <th className="pb-3">Colaborador</th>
                    <th className="pb-3">Demandas Ativas</th>
                    <th className="pb-3 text-right">Carga de Trabalho</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/50 text-sm">
                  {capacidades.map((item, index) => (
                    <tr key={index} className="hover:bg-slate-700/30 transition-colors">
                      <td className="py-3 font-medium text-slate-200">{item.colaborador}</td>
                      <td className="py-3 text-slate-300">{item.tarefas_ativas} ativas</td>
                      <td className="py-3 text-right">{renderBadgeCor(item.semaforo_capacidade)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </section>

        {/* Quadro Kanban Dinâmico */}
        <section className="space-y-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              📋 Fluxo de Trabalho (Quadro Kanban)
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">Centralização e transparência operacional sem papéis ou WhatsApp</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-stretch">
            {colunas.map((coluna) => {
              const tarefasFiltradas = tarefas.filter(t => t.status === coluna.id);

              return (
                <div key={coluna.id} className={`bg-slate-800 rounded-xl border border-slate-700 shadow-lg border-t-4 ${coluna.corBorda} flex flex-col h-full min-h-[500px]`}>
                  {/* Cabeçalho da Coluna */}
                  <div className="p-4 border-b border-slate-700/50 flex justify-between items-center bg-slate-800/50 rounded-t-xl">
                    <span className="font-bold text-sm text-slate-200">{coluna.titulo}</span>
                    <span className={`px-2 py-0.5 rounded text-xs font-black ${coluna.bgBadge}`}>
                      {tarefasFiltradas.length}
                    </span>
                  </div>

                  {/* Lista de Cartões */}
                  <div className="p-3 space-y-3 overflow-y-auto flex-1">
                    {tarefasFiltradas.map((tarefa) => (
                      <div key={tarefa.id} className="bg-slate-900 p-4 rounded-lg border border-slate-700/60 shadow-sm hover:border-slate-500 transition-all space-y-3">
                        
                        {/* Tags do Cartão */}
                        <div className="flex justify-between items-center">
                          {renderBadgePrioridade(tarefa.prioridade)}
                          <span className="text-[11px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded border border-slate-700 font-medium">
                            💼 {tarefa.nome_cliente}
                          </span>
                        </div>

                        {/* Corpo do Cartão */}
                        <div>
                          <h4 className="font-bold text-sm text-white tracking-tight">{tarefa.titulo}</h4>
                          {tarefa.descricao && (
                            <p className="text-xs text-slate-400 mt-1 line-clamp-2 leading-relaxed">{tarefa.descricao}</p>
                          )}
                        </div>

                        {/* Rodapé: Vencimento e Executores */}
                        <div className="pt-2 border-t border-slate-800/80 flex flex-col gap-2 text-[11px]">
                          <div className="flex justify-between text-slate-400">
                            <span>📅 Entrega:</span>
                            <span className="font-semibold text-slate-300">
                              {new Date(tarefa.data_entrega).toLocaleDateString('pt-BR')}
                            </span>
                          </div>
                          
                          {/* Colaboradores da Tarefa */}
                          <div className="flex flex-wrap gap-1 items-center mt-1">
                            <span className="text-slate-500 mr-0.5">👥 Time:</span>
                            {tarefa.colaboradores && tarefa.colaboradores.map((c) => (
                              <span key={c.id} className="bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded text-[10px] border border-slate-700 font-medium">
                                {c.nome.split(' ')[0]}
                              </span>
                            ))}
                            {(!tarefa.colaboradores || tarefa.colaboradores.length === 0) && (
                              <span className="text-amber-500/80 italic text-[10px]">Sem responsáveis</span>
                            )}
                          </div>
                        </div>

                      </div>
                    ))}

                    {/* Estado Vazio da Coluna */}
                    {tarefasFiltradas.length === 0 && (
                      <div className="h-32 border-2 border-dashed border-slate-700/40 rounded-xl flex items-center justify-center text-xs text-slate-500 italic">
                        Sem demandas aqui
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </section>

      </main>
    </div>
  );
}