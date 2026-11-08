# Observabilidade — métricas, saúde e logs

A fase 2 utiliza métricas HTTP da aplicação, coleta pelo Prometheus e logs de
requisição em JSON. A configuração está em
[`app/observability.py`](../app/observability.py),
[`monitoring/prometheus.yml`](../monitoring/prometheus.yml) e
[`compose.yaml`](../compose.yaml).

## Saúde e coleta

O Docker verifica `/health` da API a cada 10 segundos, com timeout de 3 segundos,
período inicial de 10 segundos e até cinco falhas consecutivas. A verificação
utiliza a biblioteca padrão do Python e confirma a resposta de saúde do SQLite;
não depende de curl na imagem. O processo Uvicorn utiliza um worker.

O Prometheus inicia depois de a API estar saudável. Seu healthcheck consulta
`/-/ready` a cada 5 segundos, com timeout de 3 segundos, período inicial de
10 segundos e até 12 tentativas. A configuração de coleta consulta
`api:8000/metrics`, job **taskflow-api**, a cada **5 segundos**. A avaliação de
regras também está configurada em 5 segundos, sem regras de alerta adicionais.

No navegador local:

- API e Swagger: `http://127.0.0.1:8000/docs`.
- Saúde com banco: `http://127.0.0.1:8000/health`.
- Exposição de métricas: `http://127.0.0.1:8000/metrics`.
- Prometheus e consulta: `http://127.0.0.1:9090`.
- Estado dos alvos: `http://127.0.0.1:9090/api/v1/targets`.

As portas podem mudar por `API_PORT` e `PROMETHEUS_PORT`, preservando o bind em
127.0.0.1. A comunicação de coleta entre containers usa a rede Docker externa.

## Métricas e cardinalidade

| Métrica | Labels | Interpretação |
|---|---|---|
| `taskflow_http_requests_total` | `method`, `route`, `status_code` | Contador de requisições HTTP concluídas ou encerradas com falha |
| `taskflow_http_request_duration_seconds_bucket` | `method`, `route`, `le` | Buckets do histograma de duração em segundos |
| `taskflow_http_request_duration_seconds_sum` | `method`, `route` | Soma das durações observadas |
| `taskflow_http_request_duration_seconds_count` | `method`, `route` | Quantidade de observações do histograma |

O middleware observa o status enviado e registra a requisição após o roteamento.
Assim, `/tasks/1` e `/tasks/2` compartilham `/tasks/{task_id}`; caminhos desconhecidos
compartilham `unmatched`. Métodos HTTP não usuais compartilham `OTHER`. IDs, títulos,
query strings e cabeçalhos não são labels. Cada aplicação criada pela factory tem
seu próprio registro de métricas, evitando contaminação entre testes/instâncias.

Consultas que podem ser usadas na interface do Prometheus:

```promql
up{job="taskflow-api"}
```

```promql
sum by (route, status_code) (rate(taskflow_http_requests_total[1m]))
```

```promql
histogram_quantile(0.95, sum by (le, route) (rate(taskflow_http_request_duration_seconds_bucket[5m])))
```

`up=1` indica sucesso da coleta do alvo. Não equivale, sozinho, a testar todo o
CRUD; por isso o smoke também consulta saúde e cria/lista/conclui uma tarefa.
Taxas e percentis precisam de amostras na janela consultada; um laboratório com
poucas requisições pode apresentar séries vazias ou percentis indefinidos.

As métricas da aplicação são mantidas em memória e reiniciam com o processo.
O Prometheus usa armazenamento em **tmpfs de 256 MiB** e retenção temporal de
**6 horas**. Esse limite temporal não garante capacidade para qualquer volume
de amostras. O histórico do Prometheus é temporário e pode desaparecer ao
recriar seu container. Isso é distinto do SQLite, persistente no volume externo.

## Logs de requisição

Cada requisição HTTP produz uma linha JSON em stdout:

| Campo | Conteúdo |
|---|---|
| `timestamp` | Instante UTC em formato ISO 8601 |
| `event` | `http_request` |
| `method` | Método HTTP normalizado |
| `route` | Rota declarada ou `unmatched` |
| `status_code` | Status observado; 500 em exceção sem resposta iniciada |
| `duration_seconds` | Duração medida por relógio monotônico, em segundos |

O middleware omite caminho bruto, ID, query string, headers e corpo. Os testes
incluem títulos, tokens de exemplo e caminhos com IDs para verificar essa omissão.
Uvicorn usa `--no-access-log`, evitando duplicar o log HTTP em outro formato.
Mensagens de inicialização e erros do servidor podem aparecer em stderr; o
Docker agrega os dois fluxos ao consultar os logs. Portanto, as linhas de eventos
HTTP são JSON, sem alegar que todas as mensagens do processo têm esse formato.

Na raiz do projeto, com `IMAGE_REF` e demais variáveis do deploy exportadas:

```bash
docker compose ps
docker compose logs --no-color --since 5m api
docker compose logs --no-color --since 5m prometheus
bash scripts/smoke.sh
```

Não existe coletor central de logs ou política de backup de logs de produção
neste laboratório. A retenção do log de containers depende da configuração do
Docker no host; as evidências da entrega são coletadas separadamente.

## Resultados e limites

Na validação local da fase 2, API e Prometheus ficaram saudáveis, o smoke
criou/listou/concluiu uma tarefa e confirmou **alvo UP e consulta up=1**. O acesso
ao volume funcionou com a API sem root. Os 38 testes Python locais passaram,
com 100% de linhas e branches. Consulte os registros e seus ambientes nas
[evidências locais](evidencias/fase2-local/).

Esses fatos locais não comprovam uma execução remota de CD. As evidências do
runner devem identificar sua própria URL, commit e digest. O monitoramento é
acadêmico, sem SLA, alerta configurado ou disponibilidade de produção prometida.
