# Checklist final — fase 1

**Situação:** implementação e validações locais concluídas. Aprovação remota do
CI e tag de fechamento pendentes por bloqueio de cobrança da conta GitHub.
O aluno solicitou registrar essa pendência; não se declara prontidão integral.

Repositório: https://github.com/Luiz-mnt/devops-taskflow

| Requisito | Arquivos/evidência real | Estado |
|---|---|---|
| Descrição, objetivos e requisitos | planejamento-fase1.md | Concluído |
| Plano CI e infraestrutura necessária | planejamento-fase1.md e ambiente-wsl.md | Concluído |
| Documento com link do repositório | Planejamento e apresentação revisada | Concluído |
| Repositório GitHub | Público, código publicado e acesso sem login verificado | Concluído |
| Pipeline GitHub Actions | ci.yml com push/PR main, jobs, gates e artefatos; actionlint aprovado | Configurado; aprovação remota pendente |
| Testes implementados e integrados | tests/, pyproject.toml, workflow; 32 testes aprovados localmente | Concluído localmente; execução CI bloqueada |
| Cobertura mínima 80% | 100% linhas/branches em Python 3.12.16, relatório real | Concluído localmente |
| Scripts IaC | infra/*.tf e lock real Windows/Linux; fmt/init/validate aprovados | Concluído |
| Provisionamento local (guia) | Apply com 2 criados, inspeções, plan posterior exit 0 em WSL2 | Concluído |
| Evidência CI aprovado e tag fase-1 (guia) | Execução 42320791079 bloqueada antes das etapas | Pendente: liberação da conta e CI verde |
| Proteção main | Checks exigidos; admin excepcionado; sem force-push/exclusão | Concluído, limitação documentada |
| Template, PDF, capturas e logs | Entrega revisada fora do repositório; capturas reais e registros locais | Preparados com pendência CI explícita |

## Encerramento

O bloqueio remanescente é externo ao código: a conta GitHub precisa liberar os
jobs. Não foram reduzidos gates, fabricados resultados ou criada tag de sucesso.
Consulte [fechar-fase1.md](fechar-fase1.md) para concluir após a liberação.
Docker/CD/Prometheus da fase 2 não são apresentados como implementados nesta fase.
