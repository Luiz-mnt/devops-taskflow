#!/usr/bin/env bash
# Smoke HTTP com biblioteca padrão; cria uma tarefa fictícia e preserva os dados.
set -euo pipefail
command -v python3 >/dev/null || { printf '%s\n' 'Python 3 é necessário no host para o smoke.' >&2; exit 1; }
export API_URL="${API_URL:-http://127.0.0.1:${API_PORT:-8000}}"
export PROMETHEUS_URL="${PROMETHEUS_URL:-http://127.0.0.1:${PROMETHEUS_PORT:-9090}}"
export SMOKE_TIMEOUT="${SMOKE_TIMEOUT:-90}"

python3 - <<'PYTHON'
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

api = os.environ['API_URL'].rstrip('/')
prometheus = os.environ['PROMETHEUS_URL'].rstrip('/')
try:
    timeout = int(os.environ['SMOKE_TIMEOUT'])
    if not 1 <= timeout <= 600:
        raise ValueError
except ValueError:
    print('SMOKE_TIMEOUT deve ser inteiro entre 1 e 600 segundos.', file=sys.stderr)
    sys.exit(2)


def request(base, path, method='GET', body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(base + path, data=data, method=method)
    if data is not None:
        req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=5) as response:
        payload = response.read().decode()
        content_type = response.headers.get('Content-Type', '')
        return response.status, json.loads(payload) if 'json' in content_type else payload


def wait_for(label, check):
    deadline = time.monotonic() + timeout
    last_error = 'resposta inesperada'
    while time.monotonic() < deadline:
        try:
            if check():
                print(label + ': OK', flush=True)
                return
        except (OSError, ValueError, KeyError, TypeError) as error:
            last_error = type(error).__name__
        time.sleep(2)
    raise RuntimeError(label + ' excedeu o prazo; último resultado: ' + last_error)


try:
    wait_for('API com SQLite saudável', lambda: request(api, '/health') == (200, {'status': 'healthy', 'database': 'ok'}))
    status, task = request(api, '/tasks', 'POST', {'title': 'Smoke ' + uuid.uuid4().hex[:12]})
    if status != 201 or task['status'] != 'pending' or not isinstance(task['id'], int):
        raise RuntimeError('Criação de tarefa não respeitou o contrato.')
    status, tasks = request(api, '/tasks')
    if status != 200 or task not in tasks:
        raise RuntimeError('Tarefa criada não encontrada na listagem.')
    status, completed = request(api, '/tasks/' + str(task['id']), 'PATCH', {'status': 'completed'})
    if status != 200 or completed != dict(task, status='completed'):
        raise RuntimeError('Conclusão de tarefa não respeitou o contrato.')
    print('CRUD criar/listar/concluir: OK (id=' + str(task['id']) + ')', flush=True)
    status, metrics = request(api, '/metrics')
    if status != 200 or 'taskflow_http_requests_total' not in metrics or 'taskflow_http_request_duration_seconds' not in metrics:
        raise RuntimeError('Métricas HTTP ausentes.')
    wait_for('Prometheus pronto', lambda: request(prometheus, '/-/ready')[0] == 200)

    def target_is_up():
        status, payload = request(prometheus, '/api/v1/targets')
        targets = payload.get('data', {}).get('activeTargets', [])
        return status == 200 and payload.get('status') == 'success' and any(
            target.get('labels', {}).get('job') == 'taskflow-api' and target.get('health') == 'up'
            for target in targets
        )

    wait_for('Alvo taskflow-api UP', target_is_up)
    query = urllib.parse.urlencode({'query': 'up{job="taskflow-api"}'})
    status, payload = request(prometheus, '/api/v1/query?' + query)
    values = payload.get('data', {}).get('result', [])
    if status != 200 or not values or not any(float(value['value'][1]) == 1 for value in values):
        raise RuntimeError('Consulta Prometheus não confirmou up=1.')
    print(json.dumps({'smoke_result': 'success', 'task_id': task['id'], 'monitoring_result': 'up=1', 'data_preserved': True}), flush=True)
except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
    print('Smoke falhou: ' + str(error), file=sys.stderr)
    sys.exit(1)
PYTHON
