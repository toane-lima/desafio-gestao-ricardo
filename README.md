# Desafio Técnico - Gestão de Atividades de um Time

Ferramenta full-stack desenvolvida sob medida para centralizar a operação, balancear a carga de trabalho do time, prever estouros de prazo e visualização de dados da empresa do Ricardo.

## 🧠 Metodologia de Gestão Escolhida e Por Quê

Afastando-nos de receitas prontas, a solução adota uma abordagem personalizada que funde os princípios visuais do **Quadro Kanban** (para centralização e fluxo transparente das demandas, eliminando o caos do WhatsApp e papel) com ciclos de revisão inspirados no **Scrum/Sprints** (mapeados através de um calendário operacional de controle semanal).

O grande diferencial estratégico do projeto é a implementação de um sistema de **Gestão Visual Unificada por Cores (Mapeamento de Semáforo)**, que atua em duas frentes críticas do dia a dia do Ricardo:

### 1. Monitoramento de Prazos das Demandas
Calculado dinamicamente com base nos dias restantes para a entrega combinada com o cliente:
🔴 **Vermelho (Crítico):** Falta **2 dias ou menos**, ou a tarefa já está atrasada.
*Impacto Gerencial:* Permite ao Ricardo agir de forma proativa, alocando reforços ou renegociando o prazo com o cliente *antes* que o estouro aconteça.
🟡 **Amarelo (Atenção):** Faltam **entre 3 e 5 dias**.
*Impacto Gerencial:* Ponto de cobrança preventiva e alinhamento do status da demanda.
🟢 **Verde (Controlado):** Faltam **mais de 5 dias** para o prazo finalizar.

### 2. Balanceamento de Carga de Trabalho (Evitando Sobrecarga e Ociosidade)
Calculado com base na quantidade de tarefas com status *A Fazer* ou *Em Andamento* sob a responsabilidade de um único colaborador:
🔴 **Vermelho (Sobrecarregado):** Colaborador com **4 ou mais tarefas** simultâneas.
*Impacto Gerencial:* Sinaliza imediatamente que o funcionário está em gargalo, proibindo novas atribuições a ele.
🟡 **Amarelo (Alerta):** Colaborador com **3 tarefas** simultâneas (limite da capacidade saudável).
🟢 **Verde (Disponível/Ocioso):** Colaborador com **0 a 2 tarefas** simultâneas.
*Impacto Gerencial:* Identifica na hora quem está livre no time para absorver novas demandas que entram na empresa.

---

## 📊 Indicadores (KPIs) e Decisões Gerenciais

Para a reunião de segunda-feira não ser baseada em achismos, o Ricardo visualizará um Dashboard dinâmico com três indicadores fundamentais:

1. **Taxa de Demandas Concluídas no Prazo (%):** Indica a eficiência preditiva do time. Se o número estiver baixo, Ricardo toma a decisão de ajustar o escopo dos projetos ou revisar o processo de estimativa de prazos da empresa.
2. **Volumetria Semanal (Solicitadas vs. Concluídas):** Apresenta o ritmo de vazão da empresa na semana. Permite ao Ricardo decidir se a empresa tem capacidade para aceitar novos clientes ou se precisa frear as vendas temporariamente.
3. **Ranking de Conclusão por Empregado:** Exibe o volume de entregas finalizadas por colaborador. Auxilia o Ricardo a identificar os perfis de alta performance e apoiar aqueles que estão com dificuldades de vazão.

---

## 🏗️ Arquitetura do Sistema e Decisões do Backend

O backend foi construído utilizando **FastAPI (Python)** e **PostgreSQL**, estruturado de forma modular e escalável para garantir separação de responsabilidades (Clean Architecture).

### 1. Modelagem do Banco de Dados & Segurança (PostgreSQL)
* **Isolamento por Esquema:** Para proteger os dados operacionais da empresa, toda a estrutura foi criada dentro de um schema próprio chamado `gestao`, separando-o do schema `public` padrão.
* **Uso de UUID v4:** Como boa prática de segurança e arquitetura distribuída, as chaves primárias dos usuários e tarefas utilizam identificadores únicos globais (`UUID`), evitando a exposição de IDs sequenciais na API.
* **Relacionamento Muitos-para-Muitos (N:M):** Implementação de uma tabela intermediária (`tarefa_colaboradores`) para permitir que uma demanda seja executada por múltiplos colaboradores simultaneamente, refletindo a realidade de projetos complexos.

### 2. Performance e Inteligência de Negócio (SQL Puro vs ORM)
* **Decisão de Engenharia:** Embora utilizemos o **SQLAlchemy** como ORM para operações de CRUD comuns (garantindo tipagem e segurança), as queries dos **Semáforos de Prazo, Capacidade e KPIs** foram escritas em **SQL Puro (`sqlalchemy.text`)**.
* **Por que fizemos isso?** Cálculos matemáticos de intervalo de datas (`data_entrega - CURRENT_DATE`), condicionais complexas (`CASE WHEN`) e agregações com agrupamento (`LEFT JOIN` com `GROUP BY`) geram um overhead imenso se processados em memória pelo Python. Ao delegar essa inteligência nativamente para o motor do PostgreSQL, reduzimos o tráfego de rede e garantimos respostas em milissegundos para o frontend.

### 3. Validação Estrita e Contratos de Dados (Pydantic)
* Utilização de Schemas do **Pydantic** para blindar a API contra dados corrompidos.
* Implementação do `EmailStr` com a biblioteca auxiliar `email-validator` para rejeitar cadastros com e-mails inválidos diretamente na camada de rede.
* Uso de contratos de resposta (`response_model`) para filtrar campos sensíveis antes que o JSON seja enviado ao cliente.

---

## 🛠️ Como Rodar o Projeto (Passo a Passo)

### 🐍 Backend (FastAPI)

#### Pré-requisitos
* Python 3.10 ou superior
* Banco de Dados PostgreSQL ativo

#### Instruções de Inicialização

1. **Navegue até a pasta do backend:**
   ```bash
   cd backend

---

2. **Crie e ative o ambiente virtual (venv):**
    python -m venv venv
    source venv/bin/activate  # No Linux/WSL2
    # venv\Scripts\activate   # No Windows

---

3. **Instale as dependências necessárias:**
    pip install -r requirements.txt

---

4. **Configuração das Variáveis de Ambiente (.env):**
    DB_USER=seu_usuario_postgres
    DB_PASSWORD=sua_senha_postgres
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=nome_do_seu_banco

---

5. **Execute o banco de dados**

---

6. **Suba o servidor Uvicorn:**
    uvicorn app.mainÇapp --reload

---

7. **Acesse a Documentação InterativaÇ**
    No navegador, digite http://127.0.0.1:8000/docs para visualizar o Swagger UI com todos os endpoints testados e validados.

---

## 🛠️ Relato Técnico: Tratamento do Relacionamento de Tarefas e Responsáveis

Durante o desenvolvimento da exibição dos colaboradores nos cartões do Quadro Kanban, foi identificado um comportamento adverso entre a camada de persistência de dados (SQLAlchemy) e a camada de serialização/validação (Pydantic) no backend.

### 🕵️‍♂️ O que foi tentado:
1. **Carregamento Antecipado (Eager Loading):** Tentativa de utilizar o método `joinedload(Tarefa.colaboradores)` na query da rota do FastAPI para trazer os relacionamentos diretamente do PostgreSQL.
2. **Queries Nativas (SQL Puro):** Implementação de busca explícita via `text()` do SQLAlchemy na tabela intermediária Many-to-Many (`gestao.tarefa_colaborador`), isolando e injetando manualmente os dicionários de usuários nas tarefas mapeadas.
3. **Flexibilização de Schemas:** Alteração dos schemas do Pydantic (`TarefaResponse`) para aceitar estruturas flexíveis (`List[dict]`), com o intuito de ignorar validações rígidas de UUID e tipos de dados no fluxo de retorno.

### 🚨 Diagnóstico & Impacto:
Apesar de a tabela intermediária no banco de dados possuir a massa de testes preenchida e consistente, todas as abordagens de junção dos dados no Python dispararam um efeito cascata no backend:
* Conflitos de validação interna geraram erros de compilação ou falhas críticas do tipo **HTTP 500 (Internal Server Error)**.
* Esses erros internos bloqueavam e derrubavam as demais requisições da API que já estavam totalmente estáveis e integradas, como os KPIs do Dashboard e os Semáforos de Capacidade.

### 💡 Decisão de Engenharia adotada:
Visando **preservar a integridade global do sistema** e respeitando a **janela de tempo estipulada para a entrega**, foi tomada a decisão de manter o backend em seu estado original estável e funcional (retornando `200 OK` limpo em todas as rotas). 

Por questões de estabilidade arquitetural nesta versão, a listagem de tarefas foi mantida sem a exibição do colaborador responsável nos cartões, garantindo que 100% das métricas de negócio, regras de semáforos, banco de dados e interface do usuário permanecessem online e integrados sem interrupções.

## 🚀 Como Executar o Projeto

### Pré-requisitos
* PostgreSQL ativo e configurado com o schema `gestao`.
* Python 3.x instalado.
* Node.js e npm instalados.

### 1. Configurando o Backend
1. Entre na pasta: `cd backend`
2. Ative o ambiente virtual: `source venv/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`
4. Inicie o servidor: `uvicorn app.main:app --reload`

### 2. Configurando o Frontend
1. Abra um novo terminal e entre na pasta: `cd frontend`
2. Instale as dependências: `npm install`
3. Inicie o app: `npm run dev`
