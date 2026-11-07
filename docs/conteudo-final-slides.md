# Conteúdo consolidado da fase 1

## Slide 1

Luiz Eduardo Santos Monteiro

TaskFlow API: Configuração e Automação Inicial

Fase 1 — validações e pendências registradas

## Slide 3

Projeto

TaskFlow API: serviço HTTP para criar, listar e concluir tarefas. Projeto acadêmico independente de sistemas empresariais.

Objetivo

Aplicar integração contínua, testes automatizados e infraestrutura como código em um laboratório reproduzível e versionado.

Requisitos funcionais

POST /tasks, GET /tasks, PATCH /tasks/{id} e GET /health. SQLite persistente, título obrigatório com até 200 caracteres e validação de entradas.

Requisitos de qualidade

Testes isolados com banco temporário, cobertura mínima de 80%, lint e formatação Ruff, dependências fixadas e configuração por ambiente.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 4

Eventos e validações

Push e pull request para main acionam jobs independentes de aplicação e infraestrutura em runners Linux hospedados pelo GitHub.

Aplicação e infraestrutura

Python 3.12, dependências fixadas, Ruff e pytest. Job Terraform: fmt -check, init -backend=false e validate. Outro job prevê apply, inspeções, plan e limpeza efêmeros.

Critérios de aprovação

Falhas de lint, testes, cobertura abaixo de 80% ou validação Terraform reprovam o CI. Relatórios JUnit e cobertura são publicados mesmo em falha.

Rastreabilidade e acesso

Execuções vinculadas ao commit. Actions fixadas por SHA, contents: read, timeout por job e sem segredos de deploy ou publicação de pacotes nesta fase.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 5

Ambiente de desenvolvimento

Windows/PowerShell e Python 3.12; Ubuntu 24.04.4 WSL2 TaskFlowDevOps com Docker Engine 29.9.3 e Terraform 1.17.1. CI hospedado configurado, mas bloqueado pela conta.

Recursos definidos como código

Provider kreuzwerker/docker: rede bridge e volume. Padrão local taskflow-net/taskflow-data; CI usa prefixo exclusivo. Lockfile versionado; estado local fora do Git.

Execução e dados

Nesta fase, API em 127.0.0.1:8000 e SQLite em caminho configurável. Rede e volume são geridos exclusivamente pelo Terraform e reservados à evolução com containers.

Escopo e capacidade

Laboratório em host único, sem nuvem contratada. Referência: 4 CPUs, 8 GB RAM e 10 GB livres. Sem alta disponibilidade ou SLA de produção.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 7

Repositório

https://github.com/Luiz-mnt/devops-taskflow

Organização implementada

app/ e tests/: aplicação e testes. infra/: Terraform. .github/workflows/ci.yml: CI. docs/: planejamento, ambiente e evidências verificáveis.

Versionamento

Branch main para integração e branches curtas para mudanças. Referência da entrega: tag fase-1 ainda não publicada. Commit publicado: 06f7bf7e72f8.

Controle de acesso

Repositório público, acessível sem login. Segredos, .env, banco, venv, .terraform/ e terraform.tfstate excluídos do versionamento. Acesso do avaliador conforme visibilidade.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

GitHub

## Slide 8

GitHub

Repositório público — captura real

Recorte da página pública real. Código, testes, workflow e Terraform publicados; CI inicial bloqueado pela conta.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 9

Workflow configurado

https://github.com/Luiz-mnt/devops-taskflow/blob/main/.github/workflows/ci.yml

Execução no GitHub Actions

Resultado: Bloqueado pela cobrança da conta, antes das etapas. https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42320791079

Testes funcionais integrados

Criação, entradas inválidas, listagem, conclusão, IDs inexistentes, saúde com acesso ao banco e persistência entre instâncias. Bancos temporários por teste.

Resultados medidos localmente

Execução LOCAL em 06/11/2026 (Windows / CPython 3.12.16 local): 32/32 testes aprovados; cobertura 100.0% de app/. Tempo medido: 2.86 s.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 10

GitHub Actions — execução bloqueada

Recorte da captura real da execução 42320791079. Os jobs não iniciaram; não há resultado verde.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 11

Causa externa registrada pelo GitHub

Recorte real: conta bloqueada por cobrança. O aluno solicitou registrar a pendência; nenhum gate foi desativado.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 12

Testes locais — Python 3.12.16

Registro real de terminal local: 32 testes aprovados, 100% de linhas e branches, em 2,86 s. CI remoto não executou testes.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 14

Código de infraestrutura

https://github.com/Luiz-mnt/devops-taskflow/tree/main/infra

Arquivos e responsabilidades

versions.tf fixa versões. main.tf cria rede e volume. variables.tf define prefixo e conexão Docker. outputs.tf expõe nomes/IDs. Lockfile gerado por init.

Procedimento de provisionamento

terraform init, fmt -check, validate, plan e apply. Inspeções Docker confirmam rede e volume; segundo plan verifica idempotência. Validação de sintaxe não cria recursos.

Resultados local e remoto

CI: Não executado: conta bloqueou os jobs. Local: Apply: 2 criados; inspeções OK; plan posterior sem alterações (exit 0). Local WSL2: No changes; exit 0.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

Terraform

## Slide 15

Terraform

Validação Terraform e workflow

Registro local: fmt, validate e actionlint aprovados. O lockfile foi gerado pelo init para Linux e Windows.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 16

Terraform

Terraform apply — WSL2 local

Registro real do laboratório TaskFlowDevOps: 2 recursos criados, 0 alterados e 0 destruídos. Rede e volume preservados.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 17

Terraform

Docker — inspeções locais reais

Registro real do Docker Engine local: taskflow-net é bridge e taskflow-data usa driver local. Inspeções com exit 0.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 18

Terraform

Terraform — plano posterior sem alterações

Registro real no WSL2 após apply: No changes; exit code 0. Idempotência comprovada sem destruir dados locais.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

## Slide 19

Verificação dos requisitos

Planejamento, código versionado, GitHub Actions, testes automatizados e scripts Terraform. Registros e links permitem reproduzir e auditar os resultados.

Atualização do documento

Documento: 07/11/2026; código 06f7bf7e72f8; Python 3.12.16; Terraform 1.17.1. Medições locais: testes 06/11/2026; IaC 06/11/2026.

Resultados observados

LOCAL em 06/11/2026: 32/32 testes aprovados; cobertura 100.0%; 2.86 s. IaC local: Apply: 2 criados; inspeções OK; plan posterior sem alterações (exit 0). CI remoto: Bloqueado pela cobrança da conta, antes das etapas.

Estado da entrega

Pendências: GitHub Actions bloqueado por cobrança da conta; aguarda liberação e execução aprovada. Tag fase-1 depende dessa aprovação.

TaskFlow API • Fase 1 • atualizado em 07/11/2026 • código 06f7bf7e72f8

Terraform
