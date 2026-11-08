# TaskFlow API — DevOps na Prática, fase 1

Aluno: **Luiz Eduardo Santos Monteiro**. Projeto acadêmico da PUCRS.

Repositório público: https://github.com/Luiz-mnt/devops-taskflow

**Fase 1 concluída e verificada:** 32 testes locais e 32 testes no GitHub Actions,
cobertura de linhas/branches 100%, Ruff e Terraform aprovados. Rede e volume
provisionados no WSL2 local; no CI, provisionamento e limpeza efêmeros aprovados.
[CI aprovado](https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42485447573) · [Tag fase-1](https://github.com/Luiz-mnt/devops-taskflow/tree/fase-1).

API de tarefas com FastAPI e SQLite, testes automatizados, integração contínua no
GitHub Actions e infraestrutura Docker descrita em Terraform. A fase 1 cobre
planejamento, CI e IaC. Containers da aplicação, Prometheus e entrega contínua
pertencem à fase 2 e não são necessários para executar esta API no ambiente virtual.

## Documentação e comprovação

- [Planejamento e requisitos](docs/planejamento-fase1.md)
- [Ambiente realmente identificado](docs/ambiente.md)
- [Checklist de entrega](docs/checklist-entrega.md)
- [Testes e cobertura](docs/evidencias/fase1-testes.md)
- [Terraform e provisionamento](docs/evidencias/fase1-infra.md)
- [Repositório e execução real do CI](docs/evidencias/fase1-github.md)
- [Resumo verificável em JSON](docs/evidencias/resumo.json)
- [Procedimento de demonstração](docs/roteiro-demonstracao.md)

## Executar no Windows (PowerShell)

Instale Python 3.12 ou utilize um Python 3.12 portátil. Os comandos abaixo partem
da raiz deste repositório; não é preciso ativar o ambiente virtual.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
$env:TASKFLOW_DB_PATH = 'data/taskflow.db'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abra http://127.0.0.1:8000/docs para o contrato OpenAPI interativo e
http://127.0.0.1:8000/health para verificar acesso ao banco.
O arquivo `.env.example` documenta a configuração; a API lê a variável do processo
e não carrega `.env` automaticamente.

No ambiente já preparado nesta pasta, `.venv` usa o Python 3.12 portátil em
`../.tools/python/`. Basta executar os comandos `.venv` acima; `py -3.12`
documenta a recriação em uma máquina com esse Python registrado no launcher.

## Executar no Linux/WSL

```bash
python3.12 -m venv .venv-linux
.venv-linux/bin/python -m pip install -r requirements-dev.txt
export TASKFLOW_DB_PATH=data/taskflow.db
.venv-linux/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

O nome `.venv-linux` preserva o ambiente `.venv` do Windows ao compartilhar a
mesma pasta pelo WSL. Ambientes virtuais não são intercambiáveis entre os sistemas.

## Contrato HTTP

| Método e rota | Entrada | Resultado |
|---|---|---|
| `POST /tasks` | `{"title":"Estudar CI"}` | 201, tarefa com `id`, título e `status: pending` |
| `GET /tasks` | — | 200, lista ordenada por ID |
| `PATCH /tasks/{id}` | `{"status":"completed"}` | 200, tarefa concluída; repetição é idempotente |
| `GET /health` | — | 200 com banco acessível; 503 se consulta ao banco falhar |

Títulos aceitam de 1 a 200 caracteres após remover espaços nas extremidades.
Entradas inválidas retornam 422. Tarefa inexistente retorna 404. A base SQLite
permanece no caminho configurado entre reinícios e é excluída do Git. Cada teste
utiliza banco temporário próprio. `/metrics` está reservado para a fase 2.

## Lint, testes e relatórios

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
```

No Linux, substitua `.\.venv\Scripts\python.exe` por `.venv-linux/bin/python`.
O `pyproject.toml` exige cobertura mínima de **80%** com medição de branches.
O pytest gera `reports/junit.xml`, `reports/coverage.xml` e `reports/htmlcov/index.html`.
O CI publica esses relatórios inclusive quando a etapa de testes falha.
Dependências e ferramentas de desenvolvimento estão fixadas nos arquivos
`requirements*.txt`; os arquivos `.in` registram as dependências diretas.

## Infraestrutura como Código

O laboratório desta entrega foi executado na distribuição WSL2 **TaskFlowDevOps**,
com Docker Engine instalado diretamente no Ubuntu. Para reproduzir neste
computador, consulte [o procedimento WSL](docs/ambiente-wsl.md). Os comandos
PowerShell abaixo são uma alternativa para instalações com Docker Desktop.

É necessário Terraform na versão de `infra/versions.tf` e Docker Engine acessível
para provisionar. No Docker Desktop, use Linux containers. O Terraform é o único
responsável pela rede bridge e pelo volume; na fase 2, Compose os consumirá como
recursos externos. Nesta fase, a API executada no ambiente virtual usa `data/`,
sem montar o volume Docker antecipadamente.

```powershell
# Windows com Docker Desktop aberto:
$env:TF_VAR_docker_host = 'npipe:////./pipe/docker_engine'
docker version
terraform -chdir=infra init -lockfile=readonly
terraform -chdir=infra fmt -check -recursive
terraform -chdir=infra validate
terraform -chdir=infra plan -out=local.tfplan
terraform -chdir=infra apply local.tfplan
docker network inspect taskflow-net
docker volume inspect taskflow-data
terraform -chdir=infra plan -detailed-exitcode
```

No WSL/Linux, use `export TF_VAR_docker_host=unix:///var/run/docker.sock` e os mesmos
comandos. O último `plan` deve encerrar com código **0** (sem alterações); **2**
significa alterações e **1** significa erro. Estado, planos, `.terraform/`, bancos e
segredos não são versionados. O `.terraform.lock.hcl` é versionado.

`terraform init -backend=false` + `terraform validate` validam dependências e a
configuração, **sem criar infraestrutura**. Somente `plan`/`apply` com Docker
acessível comprovam provisionamento. O CI está configurado para executar uma
demonstração em runner efêmero, com prefixo exclusivo e limpeza desses recursos.
Essa etapa foi aprovada na execução registrada, incluindo inspeções, plano
sem alterações e limpeza dos recursos efêmeros. O laboratório WSL2 local
foi comprovado separadamente e permanece preservado.

Não há `destroy` automático do laboratório local. Alterar o prefixo pode planejar
a substituição do volume: revise o plano antes de aplicar para preservar dados.

## Pipeline

O workflow `.github/workflows/ci.yml` executa em push e pull request para `main`.
Os jobs estão configurados para verificar qualidade/testes e formatação/validação
Terraform. Após aprovação, um push em `main` deverá demonstrar o provisionamento
em Docker no runner Linux e verificar um plano posterior sem alterações. Os
recursos remotos efêmeros têm limpeza em `always`, após coleta das evidências;
o laboratório local é independente. Nenhum job publica imagens nem utiliza
segredos de deploy. A execução remota foi aprovada e seus relatórios estão
em docs/evidencias/ci/42485447573/.

O token tem `contents: read`, as actions são fixadas por SHA e há limites de tempo.
O resultado observado e os links da execução estão na documentação de evidências.

## Limites e evolução

O projeto é um laboratório de host único: SQLite e rede/volume Docker locais.
Não oferece autenticação, alta disponibilidade, nuvem gerenciada ou implantação
pública da API. A evolução prevista inclui containers, métricas e CD na fase 2.
O checklist diferencia requisitos do enunciado e verificações adicionais do guia.

Fontes: [FastAPI](https://fastapi.tiangolo.com/),
[GitHub Actions para Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python),
[Terraform com Docker](https://developer.hashicorp.com/terraform/tutorials/docker-get-started/docker-build)
e [Docker Desktop no Windows](https://docs.docker.com/desktop/setup/install/windows-install/).
