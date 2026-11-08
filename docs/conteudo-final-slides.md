# Prévia do conteúdo dos slides — Fase 2

## Slide 1

Luiz Eduardo Santos Monteiro

TaskFlow API: entrega, monitoramento e segurança

PRÉVIA — validações em consolidação

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 2

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 3

Expansão do CI para CI/CD

CI valida código, testes e IaC; build produz a imagem; auditorias aprovadas liberam a publicação no GHCR. PR valida sem publicar; main permite entrega após os gates.

Artefato rastreável

Commit b5cc28f0fc35. A imagem aprovada é publicada e implantada pelo digest: Pendente de medição.

Deploy automatizado

Runner hospedado provisiona rede/volume com prefixo exclusivo, executa Compose pelo digest e aplica smoke tests. Coleta provas e limpa somente os recursos efêmeros.

Execução e escopo

CI do PR aprovado. Usuário optou por manter somente o PR; publicação GHCR e deploy automatizado não executados. O ambiente do runner é temporário; o laboratório local mantém seus dados. https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42511228720

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 4

Falha controlada — gate de qualidade

Recorte da captura original. Execução 42489956044: qualidade/testes falhou com exit 1; Terraform passou e o fluxo não avançou. Captura real de um PR, sem integração em main.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 5

CI do PR aprovado — sem integração

Recorte da captura original. Execução 42511228720: qualidade/testes, Terraform e build/scan aprovados. Publicação GHCR e deploy aparecem pulados; o PR permanece sem integração.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 6

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 7

Dockerfile e imagem

https://github.com/Luiz-mnt/devops-taskflow/blob/b5cc28f0fc3538779ac3f432d2c4c5aaf548619d/Dockerfile. Imagem: Pendente de medição.

Container da API

Base Python enxuta, dependências fixadas, usuário não-root, diretório /data gravável e healthcheck sem depender de curl.

Persistência e configuração

SQLite no volume externo taskflow-data; caminho por ambiente. .dockerignore exclui bancos, venv e segredos. Terraform é o único dono da rede e do volume.

Serviços coordenados

Compose conecta API e Prometheus à rede externa taskflow-net. Portas 8000 e 9090 em 127.0.0.1; recursos locais são preservados ao recriar containers.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 8

Scripts de deploy e validação

scripts/deploy.sh, scripts/smoke.sh e scripts/rollback.sh; compose.yaml configura os serviços. Links e comandos completos no README.

Fluxo de implantação

Provisionar a infraestrutura local; informar IMAGE_REF pelo digest; executar pull e compose up -d --wait com prazo limitado. Build local é um modo explícito de desenvolvimento.

Testes e persistência

Smoke: Local: saúde SQLite, criar/listar/concluir e métricas aprovados. Smoke de CD ainda não executado.. Persistência: Local inicial aprovado: tarefa id 2 preservada após recriar a API; container mudou e UID 10001 confirmado..

Reversão

Não executado: ainda não há dois digests publicados para demonstrar rollback compatível.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 9

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 10

Planejamento e aplicação na fase 1

Concluída: 32 testes e 100% de linhas/branches; CI e IaC local/remoto aprovados.

CI e infraestrutura

Referência histórica validada: fase-1 / 30b49c595e93. GitHub Actions integrado aos testes; Terraform criou rede e volume, com plano posterior sem alterações.

Evolução preservada

A fase 2 evolui o mesmo projeto. A tag fase-1 permanece imutável; métricas históricas não são substituídas pelas novas medições da aplicação instrumentada.

Rastreabilidade

https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42485447573

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 11

Entrega e deploy na fase 2

Tag ainda pendente; commit b5cc28f0fc35. Imagem imutável: Pendente de medição.

Operação local

Smoke: Local: saúde SQLite, criar/listar/concluir e métricas aprovados. Smoke de CD ainda não executado.. Monitoramento: Laboratório local: Prometheus taskflow-api UP e consulta up=1..

Segurança e permissões

pip-audit e scanner de imagem antecedem a publicação. O gate bloqueia HIGH/CRITICAL com correção disponível; vulnerabilidades sem correção permanecem identificadas nos relatórios.

Resultados observados

Ubuntu 24.04 / CPython 3.12.16, CI do PR, 08/11/2026: 38/38 testes aprovados; cobertura 100.0%; pytest 1.29 s.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 12

API local — interface OpenAPI

Recorte da captura original. Captura real inicial do laboratório local, com rotas de tarefas e saúde. Não é evidência de publicação GHCR ou CD remoto.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 13

Monitoramento e logging

Prometheus coleta /metrics; /health verifica API e SQLite. Contadores e histogramas usam rotas normalizadas. Logs JSON em stdout registram status, rota e duração sem dados sensíveis.

Segurança e limitações reais

pip-audit: 51 pacotes locais e 50 no CI do PR, zero vulnerabilidades identificadas. Trivy no PR: zero HIGH/CRITICAL corrigíveis e 42 sem correção (40 HIGH, 2 CRITICAL).

Configuração e propriedade

Versões/digest fixados e .env.example sem segredos. Terraform gerencia rede/volume; Compose gerencia containers. Estados e dados locais ficam fora do Git.

Evidências operacionais

Monitoramento: Laboratório local: Prometheus taskflow-api UP e consulta up=1.. Logs: Amostras e consultas nos registros da demonstração.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 14

Prometheus local — alvo UP

Recorte da captura original. Captura real inicial do laboratório local: alvo taskflow-api UP. A publicação da imagem e o CD em main não foram executados.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 15

Smoke local — saúde, CRUD e Prometheus

Registro de terminal real na pasta Fase 2: CRUD e alvo UP aprovados, consulta up=1. O arquivo integral está no projeto; não é captura da interface GitHub.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 16

Fluxo DevOps — visão geral

Figura 1. Dependências entre as três seções. As próximas páginas ampliam o mesmo fluxo; Mermaid, SVG e PNG integrais acompanham a entrega.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 17

GitHub Actions: CI e aprovação — parte 1/2

Figura 1-CI — parte 1/2. Mesmos nós e arestas do fluxo completo; disposição horizontal por seção. Setas no limite continuam no recorte seguinte ou anterior.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 18

GitHub Actions: CI e aprovação — parte 2/2

Figura 1-CI — parte 2/2. Mesmos nós e arestas do fluxo completo; disposição horizontal por seção. Setas no limite continuam no recorte seguinte ou anterior.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 19

GitHub Actions: entrega e demonstração temporária — parte 1/2

Figura 1-CD — parte 1/2. Mesmos nós e arestas do fluxo completo; disposição horizontal por seção. Setas no limite continuam no recorte seguinte ou anterior.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 20

GitHub Actions: entrega e demonstração temporária — parte 2/2

Figura 1-CD — parte 2/2. Mesmos nós e arestas do fluxo completo; disposição horizontal por seção. Setas no limite continuam no recorte seguinte ou anterior.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 21

Laboratório persistente no WSL2

Figura 1-LOCAL. Mesmos nós e arestas do fluxo completo; disposição horizontal por seção. Contexto de entrada preservado.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 22

Demonstração de integração

PR: https://github.com/Luiz-mnt/devops-taskflow/pull/1. Falha controlada: https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42489956044.

Aplicação e observabilidade

Deploy pelo digest; criação, listagem e conclusão de tarefa; /health; métricas e alvo Prometheus; logs JSON. A sequência e os comandos estão no roteiro de demonstração.

Persistência e recuperação

Local inicial aprovado: tarefa id 2 preservada após recriar a API; container mudou e UID 10001 confirmado.. Rollback: Não executado: ainda não há dois digests publicados para demonstrar rollback compatível..

Registros da demonstração

Resultados discriminados nos logs e nas capturas reais da entrega. Pendências: Publicação GHCR e execução do CD em main: não executadas, conforme escolha de manter o PR sem integração; Deploy local pela imagem publicada e rollback para digest anterior compatível; Tag fase-2 depois das validações remotas completas; PDF final de submissão com evidências reais do CD

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 23

Resultados medidos

CI do PR: 38 testes aprovados; 100% de linhas e branches; pytest 1,29 s no Linux. Local Windows: 38 testes e 100%, pytest 5,55 s. GHCR e CD ainda não executados.

Critérios de sucesso

Pendências: Publicação GHCR e execução do CD em main: não executadas, conforme escolha de manter o PR sem integração; Deploy local pela imagem publicada e rollback para digest anterior compatível; Tag fase-2 depois das validações remotas completas; PDF final de submissão com evidências reais do CD

Limitações

Laboratório de host único; monitoramento em tmpfs; não há implantação pública permanente. Achados de segurança sem correção são inventariados.

Melhorias futuras

Backup/restauração testados, PostgreSQL, alertas, TLS/autenticação e ambiente permanente com aprovação.

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35

## Slide 24

PRÉVIA • TaskFlow API • Fase 2 • atualizado em 08/11/2026 • código b5cc28f0fc35
