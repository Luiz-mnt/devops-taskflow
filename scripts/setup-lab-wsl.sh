#!/usr/bin/env bash
# Preparacao reproduzivel da distro isolada criada para este laboratorio.
set -euo pipefail

if [[ "${WSL_DISTRO_NAME:-}" != "TaskFlowDevOps" || "${EUID}" -ne 0 ]]; then
  printf '%s\n' 'Execute como root somente na distro WSL TaskFlowDevOps.' >&2
  exit 1
fi

source /etc/os-release
if [[ "${ID}" != "ubuntu" || "${VERSION_ID}" != "24.04" || "$(uname -m)" != "x86_64" ]]; then
  printf '%s\n' 'Este procedimento foi preparado para Ubuntu 24.04 amd64.' >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends ca-certificates curl unzip iptables procps
install -m 0755 -d /etc/apt/keyrings
curl --fail --silent --show-error --location https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
cat >/etc/apt/sources.list.d/docker.sources <<'DOCKER_REPOSITORY'
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: noble
Components: stable
Architectures: amd64
Signed-By: /etc/apt/keyrings/docker.asc
DOCKER_REPOSITORY
apt-get update
docker_package_version='5:29.9.3-1~ubuntu.24.04~noble'
apt-get install -y --no-install-recommends \
  "docker-ce=${docker_package_version}" \
  "docker-ce-cli=${docker_package_version}" \
  containerd.io docker-buildx-plugin docker-compose-plugin

terraform_version='1.17.1'
download_directory="$(mktemp -d /tmp/taskflow-terraform.XXXXXX)"
terraform_archive="terraform_${terraform_version}_linux_amd64.zip"
terraform_checksums="terraform_${terraform_version}_SHA256SUMS"
curl --fail --silent --show-error --location \
  "https://releases.hashicorp.com/terraform/${terraform_version}/${terraform_archive}" \
  -o "${download_directory}/${terraform_archive}"
curl --fail --silent --show-error --location \
  "https://releases.hashicorp.com/terraform/${terraform_version}/${terraform_checksums}" \
  -o "${download_directory}/${terraform_checksums}"
(
  cd "${download_directory}"
  grep " ${terraform_archive}$" "${terraform_checksums}" | sha256sum --check --strict
)
unzip -o "${download_directory}/${terraform_archive}" terraform -d /usr/local/bin
terraform version
docker --version
docker compose version

script_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
bash "${script_directory}/start-lab-wsl.sh"
