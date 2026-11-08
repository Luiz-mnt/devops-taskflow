# Demonstração — fase 1 concluída

1. Abra https://github.com/Luiz-mnt/devops-taskflow e apresente app/, tests/, workflow, infra/ e planejamento.
2. Abra https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42485447573. Confira os três jobs aprovados e o commit 30b49c5.
3. Mostre Ruff, 32 testes aprovados e cobertura 100% com gate mínimo 80%.
   Distinga o runner Linux (pytest 0.85 s, 08/11) do Windows local (2,86 s, 06/11).
4. Mostre infra/versions.tf, main.tf, variables.tf, outputs.tf e lockfile. O
   Terraform é responsável pela rede e pelo volume; os containers virão na fase 2.
5. No job efêmero, mostre apply com duas adições, inspeções, segundo plan sem
   alterações e cleanup de dois recursos exclusivos do runner.
6. Mostre os logs WSL2 locais: apply, inspect e plan exit 0. Os recursos locais
   permanecem criados. Para repetir a comparação, siga ambiente-wsl.md; não é
   necessário destruir nem recriar o volume.
7. Para a API local, siga o README: Uvicorn em 127.0.0.1:8000, /docs, criar,
   listar, concluir tarefa e /health com acesso ao banco. Os testes também
   comprovam persistência entre instâncias e isolamento dos bancos.
8. Abra a tag fase-1 e relacione o SHA à execução aprovada. Os documentos finais
   em main são a consolidação posterior dessa mesma implementação.

As capturas do GitHub são reais e os registros de terminal são identificados.
Não há hospedagem pública permanente da API: repositório público e runner
temporário não representam um servidor de produção. Dados locais da API ficam
no caminho TASKFLOW_DB_PATH; o volume Docker será consumido na fase 2.
