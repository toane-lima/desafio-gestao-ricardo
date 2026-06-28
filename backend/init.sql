DROP SCHEMA IF EXISTS gestao CASCADE;

CREATE SCHEMA gestao;

CREATE TABLE gestao.usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- Gera automático aqui!
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    cargo VARCHAR(50) NOT NULL,
    perfil VARCHAR(20) NOT NULL CHECK (perfil IN ('admin', 'colaborador'))
);

CREATE TABLE gestao.tarefas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- Gera automático aqui!
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    nome_cliente VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'blocked', 'done')),
    data_criacao DATE NOT NULL DEFAULT CURRENT_DATE,
    data_entrega DATE NOT NULL,
    data_conclusao DATE
);

CREATE TABLE gestao.tarefa_colaboradores (
    tarefa_id UUID REFERENCES gestao.tarefas(id) ON DELETE CASCADE,
    colaborador_id UUID REFERENCES gestao.usuarios(id) ON DELETE CASCADE,
    PRIMARY KEY (tarefa_id, colaborador_id)
);

-- Inserindo o time (Os IDs serão gerados sozinhos pelo Postgres)
INSERT INTO gestao.usuarios (nome, email, cargo, perfil) VALUES
('Ricardo Silva', 'ricardo@empresa.com', 'Dono / Administrador', 'admin'),
('Ana Souza', 'ana@empresa.com', 'Dev Backend', 'colaborador'),
('Bruno Lima', 'bruno@empresa.com', 'Designer UX/UI', 'colaborador'),
('Carlos Eduardo', 'carlos@empresa.com', 'Suporte Técnico', 'colaborador'),
('Daniela Meira', 'daniela@empresa.com', 'Dev Frontend', 'colaborador'),
('Eduardo Costa', 'eduardo@empresa.com', 'Dev Frontend', 'colaborador'),
('Fernanda Mota', 'fernanda@empresa.com', 'Dev Fullstack', 'colaborador'),
('Gabriel Rocha', 'gabriel@empresa.com', 'QA / Tester', 'colaborador'),
('Helena Reis', 'helena@empresa.com', 'Dev Ops', 'colaborador'),
('Igor Gomes', 'igor@empresa.com', 'Product Owner', 'colaborador'),
('Julia Paiva', 'julia@empresa.com', 'Social Media', 'colaborador');

-- Inserindo as Demandas (Sem passar ID também!)
INSERT INTO gestao.tarefas (titulo, descricao, nome_cliente, status, data_entrega, data_conclusao) VALUES
('Migração de Servidor Legado', 'Migrar banco para AWS', 'Cliente Alfa', 'in_progress', '2026-06-10', NULL),
('Refatoração da API de Pagamentos', 'Integrar com a nova API da Stone', 'Cliente Beta', 'in_progress', '2026-06-15', NULL),
('Criação de Prototipagem de Telas', 'Design do novo dashboard', 'Cliente Gama', 'in_progress', '2026-06-16', NULL),
('Ajuste de Bugs no Checkout', 'Corrigir falha no cupom', 'Cliente Delta', 'in_progress', '2026-06-18', NULL),
('Criação de Landing Page Natal', 'Página promocional', 'Cliente Ômega', 'todo', '2026-06-28', NULL),
('Configuração de CI/CD Pipeline', 'Automação de deploys', 'Cliente Beta', 'blocked', '2026-06-15', NULL),
('Configuração de Ambiente WSL2', 'Apoio técnico para o time', 'Interno', 'in_progress', '2026-06-16', NULL),
('Criação de Artes para Instagram', 'Postagens da semana', 'Cliente Epsilon', 'in_progress', '2026-06-16', NULL),
('Desenvolvimento de Bot Telegram', 'Processo seletivo ativo', 'Cliente Sigma', 'done', '2026-06-12', '2026-06-10'),
('Ajuste de Banco PostgreSQL', 'Criar índices para otimização', 'Cliente Zeta', 'done', '2026-06-05', '2026-06-08');

-- Vinculando os colaboradores de forma inteligente buscando pelas chaves geradas
INSERT INTO gestao.tarefa_colaboradores (tarefa_id, colaborador_id) VALUES
-- Ana Souza sobrecarregada (4 tarefas)
((SELECT id FROM gestao.tarefas WHERE titulo = 'Migração de Servidor Legado'), (SELECT id FROM gestao.usuarios WHERE email = 'ana@empresa.com')),
((SELECT id FROM gestao.tarefas WHERE titulo = 'Refatoração da API de Pagamentos'), (SELECT id FROM gestao.usuarios WHERE email = 'ana@empresa.com')),
((SELECT id FROM gestao.tarefas WHERE titulo = 'Ajuste de Bugs no Checkout'), (SELECT id FROM gestao.usuarios WHERE email = 'ana@empresa.com')),
((SELECT id FROM gestao.tarefas WHERE titulo = 'Configuração de Ambiente WSL2'), (SELECT id FROM gestao.usuarios WHERE email = 'ana@empresa.com')),

-- Bruno Cooperando com a Ana na tarefa crítica de Pagamentos
((SELECT id FROM gestao.tarefas WHERE titulo = 'Refatoração da API de Pagamentos'), (SELECT id FROM gestao.usuarios WHERE email = 'bruno@empresa.com')),
((SELECT id FROM gestao.tarefas WHERE titulo = 'Criação de Prototipagem de Telas'), (SELECT id FROM gestao.usuarios WHERE email = 'bruno@empresa.com')),

-- Helena Reis em alerta (3 tarefas)
((SELECT id FROM gestao.tarefas WHERE titulo = 'Migração de Servidor Legado'), (SELECT id FROM gestao.usuarios WHERE email = 'helena@empresa.com')),
((SELECT id FROM gestao.tarefas WHERE titulo = 'Configuração de CI/CD Pipeline'), (SELECT id FROM gestao.usuarios WHERE email = 'helena@empresa.com')),
((SELECT id FROM gestao.tarefas WHERE titulo = 'Configuração de Ambiente WSL2'), (SELECT id FROM gestao.usuarios WHERE email = 'helena@empresa.com')),

-- Julia Paiva com 1 tarefa
((SELECT id FROM gestao.tarefas WHERE titulo = 'Criação de Artes para Instagram'), (SELECT id FROM gestao.usuarios WHERE email = 'julia@empresa.com')),

-- Distribuição dos outros
((SELECT id FROM gestao.tarefas WHERE titulo = 'Criação de Prototipagem de Telas'), (SELECT id FROM gestao.usuarios WHERE email = 'daniela@empresa.com')),
((SELECT id FROM gestao.tarefas WHERE titulo = 'Criação de Landing Page Natal'), (SELECT id FROM gestao.usuarios WHERE email = 'carlos@empresa.com')),

-- Histórico de Conclusão
((SELECT id FROM gestao.tarefas WHERE titulo = 'Desenvolvimento de Bot Telegram'), (SELECT id FROM gestao.usuarios WHERE email = 'ana@empresa.com')),
((SELECT id FROM gestao.tarefas WHERE titulo = 'Ajuste de Banco PostgreSQL'), (SELECT id FROM gestao.usuarios WHERE email = 'bruno@empresa.com'));


-------------------------------------------------------------------------------
-- DOCUMENTAÇÃO: QUERIES DOS SEMÁFOROS E REQUISITOS DE NEGÓCIO (KPIs)
-- Estas consultas serão utilizadas pelo Backend (FastAPI) para alimentar o painel.
-- Nota: Considera-se o dia '2026-06-14' como a data atual simulada no sistema.
-------------------------------------------------------------------------------

-- KPI 1: Painel Geral de Métricas (Cards do Topo)
-- SELECT 
--     COUNT(*) AS total_tarefas,
--     COUNT(CASE WHEN status = 'done' THEN 1 END) AS concluidas,
--     COUNT(CASE WHEN status = 'in_progress' THEN 1 END) AS em_andamento,
--     COUNT(CASE WHEN status = 'blocked' THEN 1 END) AS bloqueadas,
--     COUNT(CASE WHEN status = 'todo' THEN 1 END) AS a_fazer,
--     COUNT(CASE WHEN status != 'done' AND data_entrega < '2026-06-14'::DATE THEN 1 END) AS vencidas
-- FROM gestao.tarefas;


-- KPI 2: Taxa de Entrega no Prazo (Gráfico de Pizza - Histórico de Performance)
-- SELECT 
--     COUNT(CASE WHEN data_conclusao <= data_entrega THEN 1 END) AS no_prazo,
--     COUNT(CASE WHEN data_conclusao > data_entrega THEN 1 END) AS fora_do_prazo,
--     ROUND((COUNT(CASE WHEN data_conclusao <= data_entrega THEN 1 END)::NUMERIC / NULLIF(COUNT(CASE WHEN status = 'done' THEN 1 END), 0)) * 100, 2) AS porcentagem_no_prazo
-- FROM gestao.tarefas;


-- KPI 3: Semáforo 1 - Prazos e Alertas Visuais das Demandas (Listagem do Kanban)
-- SELECT 
--     titulo, nome_cliente, data_entrega,
--     (data_entrega - '2026-06-14'::DATE) AS dias_restantes,
--     CASE 
--         WHEN status = 'done' THEN 'Concluído (🟢)'
--         WHEN (data_entrega - '2026-06-14'::DATE) < 0 THEN 'Atrasado (Vencido 🔴)'
--         WHEN (data_entrega - '2026-06-14'::DATE) <= 2 THEN 'Crítico (Urgente 🔴)'
--         WHEN (data_entrega - '2026-06-14'::DATE) <= 5 THEN 'Alerta (Atenção 🟡)'
--         ELSE 'No Prazo (Tranquilo 🟢)'
--     END AS semaforo_prazo
-- FROM gestao.tarefas ORDER BY data_entrega ASC;


-- KPI 4: Semáforo 2 - Carga de Trabalho e Alerta de Capacidade do Time (Gráfico de Alocação)
-- SELECT 
--     u.nome AS colaborador, COUNT(t.id) AS tarefas_ativas,
--     CASE 
--         WHEN COUNT(t.id) >= 4 THEN 'Sobrecarregado (🔴)'
--         WHEN COUNT(t.id) = 3 THEN 'No Limite (🟡)'
--         ELSE 'Disponível (🟢)'
--     END AS semaforo_capacidade
-- FROM gestao.usuarios u
-- LEFT JOIN gestao.tarefa_colaboradores tc ON u.id = tc.colaborador_id
-- LEFT JOIN gestao.tarefas t ON tc.tarefa_id = t.id AND t.status != 'done'
-- WHERE u.perfil = 'colaborador'
-- GROUP BY u.id, u.nome ORDER BY tarefas_ativas DESC;
