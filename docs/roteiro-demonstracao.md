# Roteiro de demonstração — fase 1

1. Abra o repositório indicado em `evidencias/fase1-github.md`. Mostre `app/`,
   `tests/`, `.github/workflows/ci.yml`, `infra/` e `docs/planejamento-fase1.md`.
2. Abra a execução aprovada do Actions. Confira o commit e os jobs de qualidade,
   testes, Terraform e provisionamento efêmero.
3. Mostre o relatório JUnit/cobertura e explique que o limite de 80% faz parte da
   configuração executada pelo pytest. A cobertura e o total reais estão no resumo.
4. Abra `infra/main.tf`: somente rede bridge e volume são provisionados. Mostre
   versões/lock, variáveis/prefixo e outputs. Não há containers da fase 2 neste escopo.
5. Nos logs do job de provisionamento, mostre `apply`, inspeções reais, segundo
   `plan` sem alterações e `destroy` dos recursos **efêmeros** do runner. Não afirme
   que esses recursos foram criados no Windows local.
6. Para demonstração da API, siga o README: inicie Uvicorn, abra `/docs`, crie uma
   tarefa, liste e conclua. Reinicie o processo mantendo o mesmo banco e consulte
   novamente. `/health` consulta a tabela do banco, além de verificar o processo.
7. Para comprovar provisionamento local, prepare Docker conforme `ambiente.md` e
   execute `scripts/provisionar-local.ps1`. O script requer confirmação do plano e
   não contém limpeza automática do volume local.

## Capturas sugeridas

- Repositório público com URL e diretórios visíveis.
- Actions com execução aprovada, commit e jobs.
- Relatório dos testes com total e cobertura.
- Terraform apply e plan posterior sem mudanças, identificando o ambiente.
- Se executado: Docker local com rede/volume e logs locais.

Os registros de terminal inseridos no documento são transcrições dos comandos
executados, identificadas como tal. Não são apresentados como capturas da interface
do GitHub. Não fotografe configurações contendo tokens ou credenciais.

## Explicação dos limites

O CI valida mudanças e gera evidências. A demonstração no runner é temporária;
o repositório público não hospeda a API. O banco local da fase 1 fica em `data/`.
O volume Docker será montado pela aplicação na fase 2. Alta disponibilidade,
autenticação, backup de produção e implantação pública estão fora deste escopo.
