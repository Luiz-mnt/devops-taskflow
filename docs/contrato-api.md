# Contrato HTTP — TaskFlow API

A API mantém o contrato de tarefas da fase 1 e acrescenta métricas operacionais
na fase 2. A configuração padrão do laboratório publica a API somente em
`http://127.0.0.1:8000`. O contrato interativo fica em `/docs` e sua especificação
OpenAPI em `/openapi.json`. `/metrics` é uma rota operacional documentada aqui,
sem inclusão na interface OpenAPI.

## Rotas e respostas

| Método e rota | Corpo de entrada | Resultado |
|---|---|---|
| `POST /tasks` | `{"title":"Estudar DevOps"}` | 201 com `id`, `title` e `status: pending` |
| `GET /tasks` | Nenhum | 200 com uma lista de tarefas ordenada por ID; lista vazia é `[]` |
| `PATCH /tasks/{task_id}` | `{"status":"completed"}` | 200 com a tarefa concluída; repetir a conclusão mantém o mesmo resultado |
| `GET /health` | Nenhum | 200 se o banco e a tabela estiverem acessíveis; 503 em falha da consulta |
| `GET /metrics` | Nenhum | 200 com texto no formato de exposição do Prometheus |

Uma tarefa contém somente os campos abaixo; o ID é gerado pelo SQLite:

```json
{"id":1,"title":"Estudar DevOps","status":"pending"}
```

Esse exemplo ilustra o formato, sem representar uma execução ou um ID reservado.
O campo `status` admite `pending` e `completed` na resposta. A criação sempre
inicia em `pending`; o PATCH aceita somente `completed`.

## Validação e falhas

O título deve ser uma string com 1 a 200 caracteres após remover espaços nas
extremidades. Títulos vazios, compostos somente de espaços, acima do limite ou
com caractere NUL são rejeitados. Campos adicionais no corpo, título ausente,
tipos incorretos e status de atualização inválido retornam **422**.

`task_id` deve ser um inteiro entre 1 e 9223372036854775807. Um valor fora desse
contrato retorna **422**; um ID válido sem tarefa correspondente retorna **404**
com `{"detail":"Task not found"}`. A validação não altera tarefas existentes.

O healthcheck executa uma consulta real à tabela SQLite. As respostas são:

```json
{"status":"healthy","database":"ok"}
```

ou, com HTTP 503:

```json
{"status":"unhealthy","database":"unavailable"}
```

A resposta de indisponibilidade não inclui caminhos locais nem detalhes internos
da exceção. `/health` comprova o acesso ao banco naquele momento, sem garantir
disponibilidade futura de todo o ambiente.

## Persistência e métricas

Fora do container, `TASKFLOW_DB_PATH` configura o banco e tem como padrão
`data/taskflow.db`. A aplicação lê a variável do processo, sem carregar `.env`
automaticamente. No Compose, o caminho interno é `/data/taskflow.db`, armazenado
no volume externo `${TASKFLOW_RESOURCE_PREFIX}-data`. Recriar o container da API
mantendo esse volume preserva os dados.

`/metrics` expõe `taskflow_http_requests_total` com labels `method`, `route` e
`status_code`, além do histograma `taskflow_http_request_duration_seconds` com
`method` e `route`. A rota de conclusão é registrada como `/tasks/{task_id}`;
IDs concretos e conteúdo das tarefas não viram labels. Rotas desconhecidas são
agrupadas em `unmatched`. Veja [observabilidade](observabilidade.md).

Os exemplos podem ser exercitados por `/docs` ou pelo script
[`scripts/smoke.sh`](../scripts/smoke.sh), que usa Python 3 no host, verifica
saúde, cria uma tarefa fictícia, lista, conclui e consulta o alvo do Prometheus.
O script mantém a tarefa criada e os demais dados existentes.

## Escopo e comprovação

Esta API acadêmica não oferece autenticação, TLS ou exclusão de tarefas. O acesso
de laboratório fica restrito a loopback nas portas publicadas pelo Compose.
Não exponha esse contrato diretamente como serviço público de produção.

Os 38 testes locais da fase 2 foram aprovados com 100% de cobertura de linhas e
branches. Eles verificam o contrato, persistência entre instâncias, falhas de
saúde, métricas com labels normalizados e logs sem dados de requisição. O
provisionamento, deploy e smoke locais são registrados nas
[evidências locais](evidencias/fase2-local/). Resultados de CI/CD pertencem à
execução remota identificada nas evidências correspondentes, quando observados.

Fontes da implementação: [`app/main.py`](../app/main.py),
[`app/models.py`](../app/models.py), [`app/database.py`](../app/database.py) e
[`tests/`](../tests/).
