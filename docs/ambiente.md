# Ambiente observado

Data da preparação: **06/11/2026**, fuso America/Sao_Paulo.

| Item | Resultado observado |
|---|---|
| Sistema | Windows, versão NT 10.0.26200.0, 64 bits |
| Shell | Windows PowerShell 5.1.26100.9711 |
| Git | 2.46.2.windows.1 |
| GitHub CLI | 2.86.0 |
| Conta autenticada | Luiz-mnt, confirmada com `gh api user --jq .login` |
| Python original | 3.13 em C:\\Python313; usado somente no diagnóstico inicial |
| Python do projeto | CPython 3.12.16 portátil, baixado pelo uv 0.13.7; ambiente virtual `.venv` |
| Terraform | 1.17.1, binário oficial portátil; não adicionado ao PATH global |
| Provider Docker | kreuzwerker/docker 4.6.0; lock real para windows_amd64 e linux_amd64 |
| actionlint | 1.7.12, distribuição oficial portátil, workflow validado |
| Docker inicial no Windows | Não localizado no PATH nem nos caminhos de instalação verificados |
| WSL inicial | Comando disponível; nenhuma distribuição instalada no diagnóstico inicial |
| WSL preparado | Distribuição exclusiva TaskFlowDevOps, Ubuntu 24.04.4 LTS, kernel 6.6.87.2 |
| Docker local preparado | Engine Community 29.9.3, cliente e servidor linux/amd64 confirmados no WSL2 |
| Compose local | 5.7.0; não usado no escopo da fase 1 |
| Terraform no WSL | 1.17.1, checksum oficial validado; provider Docker 4.6.0 |
| PowerPoint | Executável instalado; automação COM indisponível nesta sessão (80070520) |

Python, uv, Terraform e actionlint foram obtidos em `.tools/` da pasta de trabalho
que contém o repositório. Não pertencem ao código publicado. O SHA256 do ZIP
Terraform foi comparado com o checksum oficial:
`a3b71365cff94c0f978cf75d86addb075ea1bb6409055ea0ab359bf057d7898a`.

As primeiras consultas de rede no sandbox falharam com WinError10013, e a primeira
consulta de autenticação aparentou token inválido. Repetidas com acesso de rede
autorizado, confirmaram autenticação válida; não foi necessário novo login.
Tokens não foram copiados para o repositório nem para esta documentação.

## Laboratório local efetivamente preparado

Após explicar a preparação ao aluno, foi importada uma imagem Ubuntu Base oficial
na distribuição WSL2 dedicada `TaskFlowDevOps`. O SHA256 foi conferido:
`c1e67ef7b17a6300e136118bd1dc04725009cb376c1aad10abcf8cd453628d58`.
Dentro dela, foram instalados Docker Engine pelo repositório oficial Docker e
Terraform Linux pelo binário oficial. Não foi necessário Docker Desktop.

O daemon escuta somente `unix:///var/run/docker.sock`, sem listener TCP. O
laboratório usa configuração normal do Docker, driver overlayfs e cgroups v2.
Os recursos `taskflow-net` e `taskflow-data` foram realmente criados pelo Terraform
e preservados. O segundo plano retornou **exit 0, sem alterações**. Consulte
[evidências locais](evidencias/fase1-infra.md) e
[comandos do WSL](ambiente-wsl.md).

A API e os testes executam no Python 3.12 do ambiente virtual Windows; o Terraform
e o Docker do laboratório executam no WSL2. O cliente Docker não foi instalado
no PowerShell. `scripts/provisionar-local.ps1` é uma alternativa para máquinas
com Docker Desktop; neste laboratório, use o procedimento WSL.

## Pendência externa

O GitHub recebeu o código e o workflow, mas bloqueou os jobs antes de qualquer
etapa por uma questão de cobrança da conta. O aluno informou que não consegue
regularizar agora e solicitou registrar a pendência. Não há execução verde ou
tag `fase-1`. Não foram alteradas configurações de cobrança.

Fontes: [importação de distribuições WSL](https://learn.microsoft.com/windows/wsl/use-custom-distro),
[imagem Ubuntu oficial](https://cdimage.ubuntu.com/ubuntu-base/releases/24.04/release/),
[Docker Engine no Ubuntu](https://docs.docker.com/engine/install/ubuntu/) e
[Terraform](https://developer.hashicorp.com/terraform/install).
