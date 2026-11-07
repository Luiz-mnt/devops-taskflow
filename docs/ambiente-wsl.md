# Laboratório local WSL2 — fase 1

O provisionamento local foi executado em **06/11/2026, às 21:55, horário de São
Paulo** (07/11/2026, 00:55 UTC). A distribuição dedicada `TaskFlowDevOps` executa
Ubuntu 24.04.4 LTS em WSL2 no computador do estudante. Docker Engine foi instalado
pelo repositório APT oficial Docker; não depende de Docker Desktop. Terraform
Linux foi instalado a partir do ZIP oficial, após conferir seu SHA256.

| Componente | Versão ou configuração realmente observada |
|---|---|
| Distribuição | Ubuntu 24.04.4 LTS, amd64 |
| Kernel | 6.6.87.2-microsoft-standard-WSL2 |
| Docker cliente e servidor | 29.9.3, API 1.56 |
| containerd | 2.4.2 |
| runc | 1.5.2 |
| Docker Compose | 5.7.0 |
| Terraform | 1.17.1, linux_amd64 |
| Provider Docker | kreuzwerker/docker 4.6.0, lockfile versionado |
| Armazenamento Docker | overlayfs, cgroupfs v2 |
| API do daemon | Somente `unix:///var/run/docker.sock` |
| Processo Docker | `dockerd` normal, iniciado pelo script do laboratório |

SHA256 observado do ZIP Terraform Linux 1.17.1:

```text
4638628058e71a55212b1c563712eac03b902128f40740f3dc8174df12135061
```

Os dados e a instalação Linux permanecem no disco da distribuição WSL. Os códigos
e o estado Terraform local estão na pasta deste projeto no Windows; estado,
plano salvo e `.terraform/` são ignorados pelo Git. Os testes Python da API também
podem executar no ambiente virtual Windows documentado no README: o Docker WSL é
utilizado aqui para o provisionamento da infraestrutura.

## Iniciar novamente e verificar

Na raiz **devops-taskflow**, execute no PowerShell:

```powershell
wsl -d TaskFlowDevOps -u root -- bash scripts/start-lab-wsl.sh
wsl -d TaskFlowDevOps -u root -- docker --host unix:///var/run/docker.sock version
wsl -d TaskFlowDevOps -u root -- env TF_VAR_docker_host=unix:///var/run/docker.sock terraform -chdir=infra plan -detailed-exitcode
```

O script recusa outras distribuições e utiliza somente o socket Unix local.
Como a distribuição usa o init do WSL, a inicialização é feita explicitamente,
sem depender de `systemctl`. O script não aplica Terraform nem apaga recursos.

Para abrir o Bash no diretório atual do projeto:

```powershell
wsl -d TaskFlowDevOps -u root -- bash
```

No Bash, a sequência completa de reprodução é:

```bash
bash scripts/start-lab-wsl.sh
export DOCKER_HOST=unix:///var/run/docker.sock
export TF_VAR_docker_host=unix:///var/run/docker.sock
export TF_VAR_resource_prefix=taskflow
unset DOCKER_CONTEXT
terraform -chdir=infra init -lockfile=readonly
terraform -chdir=infra fmt -check -recursive
terraform -chdir=infra validate
terraform -chdir=infra plan -out=local.tfplan
# Confira o plano antes do apply. Não aplique exclusões de dados do laboratório.
terraform -chdir=infra apply local.tfplan
docker network inspect taskflow-net
docker volume inspect taskflow-data
terraform -chdir=infra plan -detailed-exitcode
```

O último comando deve retornar 0 para ausência de mudanças. O código 2 indica
mudanças propostas, e 1 indica erro. A execução original retornou **0**.

## Evidência observada

O primeiro plano propôs **2 adições, 0 alterações e 0 exclusões**. O apply criou
somente os seguintes recursos:

| Recurso | Resultado real |
|---|---|
| `taskflow-net` | Rede bridge local, subnet `172.18.0.0/16` |
| ID da rede | `7c5b1a6b743a72193fc27feba7e7e0e7c2636b3e7d2d4881b92601b55aecb100` |
| `taskflow-data` | Volume de driver local |
| Diretório do volume | `/var/lib/docker/volumes/taskflow-data/_data` |
| Labels de propriedade | `com.taskflow.managed-by=terraform`, ambiente `taskflow` |
| Apply | `Resources: 2 added, 0 changed, 0 destroyed.` |
| Plano posterior | `No changes. Your infrastructure matches the configuration.` |
| Exit code do plano posterior | 0 |

Os recursos permanecem criados. Não foi executado `destroy` do laboratório local.
O volume está preparado para a fase 2; o banco da API executada no ambiente
virtual ainda utiliza o caminho configurado por `TASKFLOW_DB_PATH`.

Logs originais, sem credenciais, estão em
[`evidencias/logs/`](evidencias/logs/):

- `terraform-local-ambiente.log`: versões, plataforma e hash do ZIP.
- `terraform-local-init.log` e `terraform-local-validate.log`: inicialização e validação.
- `terraform-local-plan.log`: plano anterior ao provisionamento.
- `terraform-local-apply.log`: criação real dos dois recursos.
- `terraform-local-inspect.log`: inspeções Docker e outputs Terraform.
- `terraform-local-outputs.json`: outputs estruturados.
- `terraform-local-plan-after.log`: comparação posterior sem alterações e exit code.

## Preparação da distribuição

O script [`scripts/setup-lab-wsl.sh`](../scripts/setup-lab-wsl.sh) registra a
instalação utilizada. Ele pressupõe que a distribuição `TaskFlowDevOps` já existe
e recusa executar fora dela. Instala os pacotes pelo repositório oficial Docker,
fixa Docker Engine/CLI em 29.9.3 e Terraform em 1.17.1, verifica o checksum do ZIP e
inicia o daemon local. Não altera outras distribuições, não configura listener
TCP e não executa Terraform apply/destroy.

Fontes técnicas utilizadas:
[Docker Engine no Ubuntu](https://docs.docker.com/engine/install/ubuntu/),
[release oficial Terraform 1.17.1](https://releases.hashicorp.com/terraform/1.17.1/)
e [Terraform com Docker](https://developer.hashicorp.com/terraform/tutorials/docker-get-started/docker-build).
