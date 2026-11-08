# Roteiro de demonstração — fase 2

Abra Fase 2/devops-taskflow. A implementação da fase 1 pode ser consultada pela
tag fase-1. Utilize dados fictícios e não mostre credenciais ao gravar capturas.
As etapas de publicação e rollback devem ser marcadas pendentes até executadas.

## 1. Histórico, PR e gates

1. Mostre o planejamento e o código da tag fase-1.
2. Mostre o PR #1, a falha intencional da execução 42489956044 e o bloqueio do CI.
3. Mostre a remoção do teste controlado e a execução corrigida 42511228720:
   qualidade/testes, Terraform e build/scan aprovados; publicação omitida em PR.
4. Após a integração autorizada, mostre o run de main e os jobs encadeados,
   os relatórios, o digest no GHCR e o deploy temporário. Não trate a execução
   de PR como prova de publicação ou de CD.

## 2. Laboratório e configuração

No PowerShell, dentro da raiz do projeto:

```powershell
wsl -d TaskFlowDevOps -u root -- bash scripts/start-lab-wsl.sh
wsl -d TaskFlowDevOps -u root -- bash
```

No Bash, confira o estado existente sem excluir dados:

```bash
export TF_VAR_docker_host=unix:///var/run/docker.sock
export TF_VAR_resource_prefix=taskflow
export TASKFLOW_RESOURCE_PREFIX=taskflow
terraform -chdir=infra plan -detailed-exitcode
docker network inspect taskflow-net
docker volume inspect taskflow-data
```

O estado ativo é o da fase 2. Não aplique simultaneamente a cópia antiga da
fase 1 para os mesmos recursos. Nunca use destroy para demonstrar persistência.

## 3. Deploy pela imagem publicada

Execute esta etapa somente depois de image_ref existir no resumo aprovado:

```bash
export IMAGE_REF="$(python3 -c 'import json; r=json.load(open("docs/evidencias/resumo.json")); assert r["image_ref"]; print(r["image_ref"])')"
docker pull "$IMAGE_REF"
bash scripts/deploy.sh
bash scripts/smoke.sh
docker compose ps
docker compose logs --tail 30 api
```

Pacotes públicos permitem pull sem login. Se o pacote for privado, autentique
pelo procedimento oficial com read:packages, no terminal, sem incluir token
em arquivos ou na conversa. O deploy faz pull por digest e não reconstrói.

Alternativa inicial sem registry: docker build --tag taskflow-local:teste .;
defina IMAGE_REF=taskflow-local:teste, baixe Prometheus uma vez e use
IMAGE_PULL_POLICY=never bash scripts/deploy.sh. Identifique essa prova como local.

## 4. Métricas, logs e persistência

Abra http://127.0.0.1:8000/docs e crie/conclua uma tarefa fictícia. Mostre
/health, /metrics e os logs JSON, sem conteúdo da tarefa. No Prometheus,
http://127.0.0.1:9090/targets deve mostrar o alvo taskflow-api UP; consulte
up{job="taskflow-api"}. Mostre que IDs não aparecem nos rótulos das rotas.

Guarde o id/título/status de uma tarefa da listagem, recrie a API com
docker compose up -d --no-deps --force-recreate --wait api e consulte a listagem
novamente. Confirme que o container mudou e a mesma tarefa permaneceu. O smoke
sozinho cria uma tarefa nova e não substitui esse teste de persistência.

## 5. Rollback compatível e encerramento

Quando houver dois digests publicados e compatíveis, implante o novo, registre
o digest/estado dos dados e execute bash scripts/rollback.sh com o digest
anterior. Confirme saúde, CRUD, Prometheus e preservação da tarefa original.
Registre os dois digests reais e o resultado. Rollback não reverte o banco.

Para encerrar containers locais preservando os dados, use docker compose down.
Rede e volume são externos e continuam sob Terraform. A limpeza automática
com destroy aparece somente no runner efêmero, depois da coleta das provas.
