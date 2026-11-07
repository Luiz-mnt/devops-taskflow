#!/usr/bin/env bash
# Inicia somente o Docker da distribuicao WSL dedicada ao projeto.
set -euo pipefail

if [[ "${WSL_DISTRO_NAME:-}" != "TaskFlowDevOps" ]]; then
  printf '%s\n' 'Execute este script na distribuicao WSL TaskFlowDevOps.' >&2
  exit 1
fi

if [[ "${EUID}" -ne 0 ]]; then
  printf '%s\n' 'Execute com wsl -d TaskFlowDevOps -u root -- bash scripts/start-lab-wsl.sh' >&2
  exit 1
fi

export DOCKER_HOST=unix:///var/run/docker.sock
unset DOCKER_CONTEXT
if docker info >/dev/null 2>&1; then
  printf '%s\n' 'Docker local ja esta disponivel.'
  exit 0
fi

# Sem listener TCP. Os dados permanecem em /var/lib/docker nesta distro.
nohup dockerd --host=unix:///var/run/docker.sock >/var/log/taskflow-dockerd.log 2>&1 </dev/null &

for attempt in {1..30}; do
  if docker info >/dev/null 2>&1; then
    printf '%s\n' 'Docker local iniciado; socket unix:///var/run/docker.sock.'
    exit 0
  fi
  sleep 1
done

printf '%s\n' 'Docker nao iniciou em 30 segundos. Consulte /var/log/taskflow-dockerd.log.' >&2
tail -n 40 /var/log/taskflow-dockerd.log >&2
exit 1
