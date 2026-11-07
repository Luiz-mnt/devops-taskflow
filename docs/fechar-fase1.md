# Encerrar a fase 1 após liberar o GitHub Actions

Neste momento, a conta bloqueia os jobs antes das etapas por questão de cobrança.
O aluno solicitou manter a pendência registrada. O código, testes, workflow e
Terraform já estão publicados; os testes e o provisionamento local foram aprovados.
Não é necessário refazer o projeto.

## 1. Liberar a execução

O titular deve verificar a situação em https://github.com/settings/billing.
Não copie dados de pagamento nem tokens para o projeto ou a conversa.

Após a liberação, na raiz do repositório, dispare o workflow no commit atual:

```powershell
gh workflow run ci.yml --repo Luiz-mnt/devops-taskflow --ref main
```

Abra https://github.com/Luiz-mnt/devops-taskflow/actions e acompanhe a nova
execução manual. Ela deve aprovar os jobs **Qualidade e testes**, **Terraform** e
**Provisionamento efemero**. Para acompanhar pela CLI, obtenha a execução manual
mais recente (confira se é a que acabou de iniciar):

```powershell
$runs = gh run list --repo Luiz-mnt/devops-taskflow --workflow ci.yml --event workflow_dispatch --branch main --limit 1 --json databaseId,headSha,status,url | ConvertFrom-Json
$run = $runs[0]
$run | Format-List
gh run watch $run.databaseId --repo Luiz-mnt/devops-taskflow --exit-status
if ($LASTEXITCODE -ne 0) { throw 'CI nao aprovado: consulte logs e corrija antes de fechar a fase.' }
gh run download $run.databaseId --repo Luiz-mnt/devops-taskflow --dir reports/github
```

Se os jobs iniciarem e falharem, corrija a causa e publique novo commit mantendo
os gates. Não transforme o registro de bloqueio atual em sucesso sem execução real.
O `phase1_commit` deve identificar o commit efetivamente aprovado.

## 2. Registrar a aprovação e criar a tag

Confira o SHA, os relatórios JUnit/cobertura e os logs remotos de apply/inspect,
plano sem alterações e cleanup. Preserve a evidência local já coletada.
Somente após aprovação, crie a tag no SHA dessa execução:

```powershell
git fetch origin main --tags
git show-ref --verify --quiet refs/tags/fase-1
if ($LASTEXITCODE -eq 0) { throw 'A tag fase-1 ja existe: confira seu destino sem move-la.' }
git tag -a fase-1 $run.headSha -m 'Fase 1: commit aprovado pelo GitHub Actions'
git push origin fase-1
```

## 3. Atualizar o documento

Atualize `docs/evidencias/fase1-github.md`, `resumo.json` e `checklist-entrega.md`
com URL, SHA, tag, conclusão e métricas realmente medidas. Diferencie os testes
locais dos remotos; o tempo local de 2,86 s não é a duração do runner.
No JSON, preencha `phase1_commit`, `ci_run_url`, `ci_head_sha`, `ci_conclusion`,
`ci_test_count`, `ci_coverage_percent`, `terraform_ci_result`, `phase1_tag`/`tag`
e remova a pendência somente depois de verificar todos os resultados.
`delivery_ready` só pode ser `true` quando não houver requisito pendente.

As fontes locais da apresentação estão em
`../entrega-fase1/ferramentas/gerar_entrega.py`, fora do repositório. Na pasta
**Fase 1**, com Pillow e PyMuPDF disponíveis, execute:

```powershell
python entrega-fase1/ferramentas/gerar_entrega.py
```

Substitua as capturas do CI bloqueado por capturas reais da execução aprovada,
ajustando `presentation_evidence` no resumo. Revise o PDF, os links e a ausência
de placeholders antes de submetê-lo. Publique também os documentos atualizados.

A [documentação oficial sobre reexecução](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs)
permite reexecutar uma tentativa mantendo seu SHA original. O procedimento acima
prefere uma execução manual em `main` para verificar a revisão atual.
