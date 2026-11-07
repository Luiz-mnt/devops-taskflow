# GitHub e CI — configuração publicada; aprovação remota pendente

- Repositório público: https://github.com/Luiz-mnt/devops-taskflow
- Workflow: https://github.com/Luiz-mnt/devops-taskflow/blob/main/.github/workflows/ci.yml
- Scripts IaC: https://github.com/Luiz-mnt/devops-taskflow/tree/main/infra
- Execução efetivamente consultada: https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42320791079
- Commit dessa tentativa: `06f7bf7e72f8358912000347ca120980c52bab49`
- Conclusão registrada pelo GitHub: **failure**, antes de executar qualquer etapa.
- Testes/cobertura remotos: **não medidos**, pois nenhum job iniciou.
- Tag `fase-1`: **não criada**, pois depende de CI aprovado conforme o guia.

## Reverifica??o em 07/11/2026

Foi executada uma segunda tentativa real do mesmo workflow/commit. O GitHub
voltou a bloquear os jobs antes de qualquer etapa, pela mesma quest?o de cobran?a.
A tentativa 2 est? registrada nos JSONs e no log CLI; as capturas preservam a
tentativa original, com a mesma mensagem de bloqueio. N?o h? execu??o aprovada.

## Motivo observado

As anotações dos jobs de qualidade e Terraform apresentam:

> The job was not started because your account is locked due to a billing issue.

O job de provisionamento foi pulado porque depende dos anteriores. Não existem
logs de etapas nem artefatos remotos de testes nessa execução. Não é uma falha de
teste observada; também não é possível afirmar aprovação remota do código.
O aluno informou que não consegue regularizar agora e solicitou registrar a
pendência. Nenhum dado de pagamento foi solicitado ou alterado.

Registros: [execução e jobs](github-execucao.json),
[anotação original](github-anotacoes.json),
[contexto do bloqueio](github-bloqueio.json),
[capturas reais](imagens/) e [consulta CLI](logs/github-run.log).

## Validações locais já aprovadas

32 testes, cobertura de linhas/branches 100%, Ruff, Terraform fmt/init/validate,
actionlint e provisionamento real no WSL2 com plano posterior sem alterações.
Esses resultados são **locais**, não atribuídos ao runner GitHub.
O código da API, os testes e as dependências correspondem ao commit acima; os
commits posteriores consolidam evidências e ajustes do procedimento de laboratório.

## Acesso e proteção de main

A API e o navegador sem login confirmaram o repositório público. O professor pode
acessar os arquivos sem convite. Main está protegida com os checks **Qualidade e
testes** e **Terraform** exigidos, branch atualizada, histórico linear, force-push
e exclusão desabilitados. A exceção de administrador permanece habilitada
(`enforce_admins: false`) para viabilizar o trabalho individual. Portanto, o dono
pode publicar alterações administrativas mesmo enquanto os checks estão
bloqueados; isso não equivale a aprovação dos checks.

Estado real: [proteção consultada pela API](github-protecao-main.json).
As permissões do workflow são `contents: read`; actions fixadas por SHA; PR não
publica imagens nem utiliza segredos de deploy.

## Como encerrar a pendência

Após o aluno resolver a situação da conta em suas configurações do GitHub,
execute o procedimento [fechar fase 1](../fechar-fase1.md). Confirme o CI aprovado,
baixe seus relatórios, atualize as métricas remotas separadamente e só então crie
a tag `fase-1` no commit aprovado, sem mover tag existente. Atualize PPTX/PDF com
essa prova. Até isso ocorrer, a fase não é declarada integralmente concluída.
