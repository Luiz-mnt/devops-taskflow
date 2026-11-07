# Roteiro de demonstração — fase 1

1. Abra o repositório indicado em `evidencias/fase1-github.md`. Mostre `app/`,
   `tests/`, `.github/workflows/ci.yml`, `infra/` e `docs/planejamento-fase1.md`.
2. Abra a execução do Actions registrada nas evidências. Ela foi bloqueada antes
   das etapas por uma questão de cobrança da conta. Mostre a mensagem real;
   não a apresente como execução aprovada. Depois da liberação da conta, execute
   o CI e confira commit/jobs antes de atualizar o documento.
3. Mostre o relatório JUnit/cobertura e explique que o limite de 80% faz parte da
   configuração executada pelo pytest. A cobertura e o total reais estão no resumo.
4. Abra `infra/main.tf`: somente rede bridge e volume são provisionados. Mostre
   versões/lock, variáveis/prefixo e outputs. Não há containers da fase 2 neste escopo.
5. Nos logs **locais WSL2**, mostre `apply` com dois recursos criados, inspeções e
   segundo `plan` sem alterações (exit 0). A rede/volume locais foram preservados.
   O provisionamento remoto efêmero está apenas configurado; não executou devido
   ao bloqueio da conta. Seu `destroy` é restrito ao runner, quando puder executar.
6. Para demonstração da API, siga o README: inicie Uvicorn, abra `/docs`, crie uma
   tarefa, liste e conclua. Reinicie o processo mantendo o mesmo banco e consulte
   novamente. `/health` consulta a tabela do banco, além de verificar o processo.
7. Para repetir a verificação local, siga `ambiente-wsl.md`: inicie o daemon na
   distribuição `TaskFlowDevOps` e execute `plan -detailed-exitcode`. O ambiente
   já está preparado e os recursos continuam criados. Não é necessário reaplicar
   nem destruir o volume para demonstrar o resultado.

## Capturas sugeridas

- Repositório público com URL e diretórios visíveis.
- Actions com bloqueio real, commit e anotações; substituir por execução aprovada após regularização.
- Relatório dos testes com total e cobertura.
- Terraform apply e plan posterior sem mudanças, identificando o ambiente.
- Docker local com rede/volume e logs locais reais já coletados.

Os registros de terminal inseridos no documento são transcrições dos comandos
executados, identificadas como tal. Não são apresentados como capturas da interface
do GitHub. Não fotografe configurações contendo tokens ou credenciais.

## Explicação dos limites

O CI valida mudanças e gera evidências. A demonstração no runner é temporária;
o repositório público não hospeda a API. O banco local da fase 1 fica em `data/`.
O volume Docker será montado pela aplicação na fase 2. Alta disponibilidade,
autenticação, backup de produção e implantação pública estão fora deste escopo.
