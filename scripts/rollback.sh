#!/usr/bin/env bash
# Reimplanta um digest anterior compatível. Não reverte o banco SQLite.
set -euo pipefail

if [[ "$#" -ne 1 || ! "$1" =~ @sha256:[a-f0-9]{64}$ ]]; then
  printf '%s\n' 'Uso: bash scripts/rollback.sh imagem@sha256:<digest-anterior-compatível>' >&2
  exit 2
fi

script_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
printf '%s\n' 'Rollback da imagem: o banco e os dados existentes serão preservados, sem reversão de esquema.'
bash "${script_directory}/deploy.sh" "$1"
bash "${script_directory}/smoke.sh"
