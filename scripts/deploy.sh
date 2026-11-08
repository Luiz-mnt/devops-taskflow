#!/usr/bin/env bash
# Implanta somente containers; rede e volume continuam sob propriedade Terraform.
set -euo pipefail

project_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${project_directory}"

if [[ "$#" -gt 1 ]]; then
  printf '%s\n' 'Uso: bash scripts/deploy.sh [IMAGE_REF]' >&2
  exit 2
fi

export IMAGE_REF="${1:-${IMAGE_REF:-}}"
export IMAGE_PULL_POLICY="${IMAGE_PULL_POLICY:-always}"
export TASKFLOW_RESOURCE_PREFIX="${TASKFLOW_RESOURCE_PREFIX:-taskflow}"
wait_timeout="${DEPLOY_TIMEOUT:-120}"

if [[ -z "${IMAGE_REF}" || "${IMAGE_REF}" == -* || "${IMAGE_REF}" =~ [[:space:]] ]]; then
  printf '%s\n' 'Defina IMAGE_REF sem espaços, com tag explícita ou digest sha256.' >&2
  exit 2
fi
if [[ "${IMAGE_REF}" != *@sha256:* && "${IMAGE_REF##*/}" != *:* ]]; then
  printf '%s\n' 'A imagem precisa de tag explícita ou digest sha256.' >&2
  exit 2
fi
if [[ "${IMAGE_REF}" == *@* && ! "${IMAGE_REF}" =~ @sha256:[a-f0-9]{64}$ ]]; then
  printf '%s\n' 'Digest inválido: use imagem@sha256: seguido de 64 caracteres hexadecimais.' >&2
  exit 2
fi
if [[ "${IMAGE_PULL_POLICY}" != always && "${IMAGE_PULL_POLICY}" != never ]]; then
  printf '%s\n' 'IMAGE_PULL_POLICY deve ser always (registro) ou never (teste local).' >&2
  exit 2
fi
if [[ ! "${TASKFLOW_RESOURCE_PREFIX}" =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ || "${#TASKFLOW_RESOURCE_PREFIX}" -gt 40 ]]; then
  printf '%s\n' 'TASKFLOW_RESOURCE_PREFIX inválido; use o mesmo prefixo do Terraform.' >&2
  exit 2
fi
if [[ ! "${wait_timeout}" =~ ^[1-9][0-9]*$ || "${wait_timeout}" -gt 600 ]]; then
  printf '%s\n' 'DEPLOY_TIMEOUT deve ser um inteiro de 1 a 600 segundos.' >&2
  exit 2
fi

command -v docker >/dev/null || { printf '%s\n' 'Docker não encontrado.' >&2; exit 1; }
docker compose version >/dev/null
[[ "$(docker info --format '{{.OSType}}')" == linux ]] || { printf '%s\n' 'Docker Linux indisponível.' >&2; exit 1; }
docker network inspect "${TASKFLOW_RESOURCE_PREFIX}-net" >/dev/null
docker volume inspect "${TASKFLOW_RESOURCE_PREFIX}-data" >/dev/null
docker compose config --quiet

if [[ "${IMAGE_PULL_POLICY}" == always ]]; then
  docker compose pull
else
  while IFS= read -r local_image; do
    if ! docker image inspect "${local_image}" >/dev/null 2>&1; then
      printf 'Imagem local ausente: %s. Construa/carregue a API e faça o pull explícito do Prometheus antes do modo never.\n' "${local_image}" >&2
      exit 1
    fi
  done < <(docker compose config --images)
fi

docker compose up -d --no-build --pull never --wait --wait-timeout "${wait_timeout}"
docker compose ps
printf '%s\n' 'Deploy concluído. Execute bash scripts/smoke.sh para verificar API e Prometheus.'
