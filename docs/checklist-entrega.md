# Checklist de entrega — fase 2 mantida em PR, sem integração

A fase 1 está concluída e preservada na tag fase-1. Os resultados locais da
fase 2 estão registrados; a aprovação remota e os documentos finais ainda serão
consolidados. O estudante escolheu manter somente o PR, sem merge. Este checklist não declara a fase 2 pronta para submissão.

| Requisito | Arquivo / evidência | Situação |
|---|---|---|
| Expandir CI para CD | .github/workflows/ci.yml | CI do PR aprovado; CD não executado por escolha de não integrar |
| Dockerfile não-root | Dockerfile | Build e deploy locais aprovados |
| Orquestração e scripts de deploy | compose.yaml e scripts/*.sh | Smoke local aprovado |
| Monitoramento e logs | app/observability.py, monitoring/, docs/observabilidade.md | UP=1 e JSON locais confirmados |
| Testes integrados | tests/ e reports/ | 38 locais e 38 no PR; 100% de linhas/branches |
| Segurança | pip-audit, Trivy e gate obrigatório | PR: pip-audit/scan aprovados; achados sem correção registrados |
| Infraestrutura e persistência | infra/, volume externo | Plan local exit 0; tarefa preservada após recriar API |
| Publicação por digest | GHCR e job publish | Pendente de execução real |
| Deploy por digest e rollback | scripts/deploy.sh e rollback.sh | Pendente de validação com imagem publicada |
| Falha controlada | Execução 42489956044 do PR #1 | Bloqueio confirmado; correção em validação |
| Fluxograma completo | docs/fluxograma.mmd | Fonte preparada; revisar e exportar |
| Relatório final e PDF no template | entrega-fase2/ | Em preparação |
| Tag fase-2 | Commit aprovado | Pendente após validação |

O enunciado requer o pipeline de CD, o fluxograma e o relatório final em PDF.
O guia acrescenta demonstrações reais de persistência, falha controlada e
rollback quando houver duas versões compatíveis. Não há limpeza automática
de dados locais. O deploy no runner é temporário.
