# Planejamento — fase 1: Configuração e Automação Inicial

**Aluno:** Luiz Eduardo Santos Monteiro

**Disciplina:** DevOps na Prática — PUCRS

**Projeto:** TaskFlow API

**Data de preparação:** 06/11/2026

## 1. Descrição do projeto, objetivos e requisitos

A TaskFlow API gerencia tarefas por HTTP. O usuário cria uma tarefa, consulta a
lista e marca uma tarefa como concluída. Os dados persistem em SQLite. O escopo
reduzido permite demonstrar mudanças versionadas, qualidade automatizada e
infraestrutura reproduzível sem contratação de serviços de nuvem.

Os objetivos são automatizar a verificação de cada alteração, detectar regressões
antes da integração em `main`, registrar resultados rastreáveis por commit e
representar a infraestrutura como código revisável e reprodutível.

| ID | Requisito | Critério de aceite |
|---|---|---|
| RF01 | Criar tarefa com título obrigatório | POST retorna 201, ID e status pending; título vazio/espaços/>200 é rejeitado |
| RF02 | Listar tarefas | GET retorna 200 e lista ordenada por ID |
| RF03 | Concluir tarefa | PATCH retorna completed; ID desconhecido retorna 404; entrada inválida retorna 422 |
| RF04 | Consultar saúde e persistir dados | /health consulta tabela SQLite; nova instância recupera tarefas salvas |
| RNF01 | Testes isolados | Cada teste utiliza diretório e banco temporários, sem contaminar outros testes |
| RNF02 | Qualidade automatizada | Ruff e testes aprovados, cobertura de app/ >=80% incluindo branches |
| RNF03 | Reprodutibilidade | Python 3.12, dependências fixadas, Terraform/provider fixados e lock versionado |
| RNF04 | Proteção de dados | Sem credenciais, estado Terraform ou bancos no Git; API somente em loopback por padrão |
| RNF05 | Rastreabilidade | Repositório acessível ao professor, workflow, execução e commit registrados |
| RNF06 | Infraestrutura declarativa | Rede bridge e volume definidos em Terraform com prefixo configurável |

## 2. Plano de integração contínua

Fluxo: branch de alteração → commit → push/pull request para `main` → GitHub
Actions → Ruff + testes/cobertura e validação IaC → relatórios → correção em caso
de falha. Um push aprovado em `main` também provisiona recursos Docker efêmeros
no runner, comprova ausência de alterações no segundo plano e os remove ao final.

| Etapa | Ferramenta | Aprovação |
|---|---|---|
| Obter fonte e ambiente | Checkout, setup-python | Commit correto e Python 3.12 |
| Instalar dependências | pip + requirements-dev.txt | Instalação de versões fixadas sem erro |
| Estilo e erros estáticos | Ruff check e format --check | Exit code 0 |
| Testes automatizados | pytest + pytest-cov | Todos aprovados e cobertura >=80% |
| Publicar relatórios | upload-artifact em always | JUnit, cobertura XML/HTML disponíveis quando gerados |
| Verificar IaC | Terraform fmt/init/validate | Sem erro de formato ou configuração |
| Demonstrar provisionamento em main | Terraform + Docker | Apply aprovado; inspect; plano posterior sem mudanças |
| Limpar laboratório do runner | Terraform destroy em always | Somente prefixo efêmero desse runner |

Execuções usam runner hospedado Ubuntu, limites de tempo e permissão mínima
`contents: read`. Pull requests não publicam imagens nem acessam segredos de
deploy. Não se usa `pull_request_target`. Uma falha interrompe os gates; o autor
corrige e faz novo commit. Os logs preservam a evidência da falha.

A integração individual pode ocorrer por push em `main`; branches/PR são o fluxo
recomendado para evolução. A proteção de branch depende das configurações reais
registradas em `evidencias/fase1-github.md`, sem presumir que existe.

## 3. Especificação de infraestrutura

| Componente | Especificação | Responsável |
|---|---|---|
| Host de desenvolvimento | Windows + PowerShell; WSL2/Linux sugerido para fase 2 | Estudante |
| Runtime da API | Python 3.12 + FastAPI/Uvicorn; 127.0.0.1:8000 | Ambiente virtual nesta fase |
| Persistência da API local | SQLite em TASKFLOW_DB_PATH, padrão data/taskflow.db | Aplicação |
| Rede Docker | Bridge `${resource_prefix}-net`, padrão taskflow-net | Terraform |
| Volume Docker | Volume `${resource_prefix}-data`, padrão taskflow-data | Terraform |
| Provedor IaC | kreuzwerker/docker e Terraform com versões exatas em versions.tf | Terraform |
| Estado IaC | Local por ambiente; fora do Git | Operador |
| Laboratório CI | Docker no runner Ubuntu, prefixo único por execução/tentativa | GitHub Actions |
| Containers e observabilidade | Previsto para fase 2; consumirão rede/volume como external | Docker Compose, futuramente |

Não há instâncias de nuvem, Kubernetes, IP público ou portas publicadas pelo
Terraform da fase 1. A rede e o volume preparam a infraestrutura para a fase 2.
O volume ainda não armazena o banco da API executada no ambiente virtual.
O tamanho e a capacidade dependem do host Docker. O laboratório não representa
alta disponibilidade nem uma infraestrutura de produção.

## 4. Verificação e entrega

O documento da disciplina deve apontar para o repositório, workflow e `infra/`.
Links reais, execuções, métricas e limitações são registrados em
[evidências do GitHub](evidencias/fase1-github.md) e
[resumo verificável](evidencias/resumo.json), após execução.

Os requisitos do enunciado são planejamento, GitHub, GitHub Actions, scripts IaC
e testes integrados. O guia acrescenta evidência de apply local, inspeções e
plano posterior sem alterações. Esse item adicional permanece pendente se não
houver daemon Docker local: validação sintática e apply no runner não o substituem.

O [checklist de entrega](checklist-entrega.md) relaciona cada requisito aos
arquivos e resultados observados. Não são utilizadas métricas, capturas ou URLs
de execução inventadas.
