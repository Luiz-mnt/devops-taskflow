# Checklist final — fase 1 concluída

**Situação verificada em 08/11/2026:** planejamento, implementação, testes locais,
CI real, scripts IaC, provisionamento local/remoto, evidências e tag concluídos.
Repositório: https://github.com/Luiz-mnt/devops-taskflow

| Requisito | Arquivos e prova | Estado |
|---|---|---|
| Descrição, objetivos e requisitos | planejamento-fase1.md | Concluído |
| Plano de integração contínua | Planejamento e .github/workflows/ci.yml | Concluído |
| Especificação da infraestrutura | Planejamento, infra/*.tf e ambiente-wsl.md | Concluído |
| Documento com links de repositório/CI/IaC | Planejamento e apresentação final | Concluído |
| Repositório GitHub | Público e acessível ao avaliador | Concluído |
| Pipeline GitHub Actions | Execução 42485447573: três jobs aprovados | Concluído |
| Testes automatizados implementados e integrados | 32 testes locais e 32 no CI, sem falhas | Concluído |
| Cobertura mínima 80% | 100% de linhas e branches nos dois ambientes | Concluído |
| Scripts IaC e lock real | Terraform 1.17.1/provider 4.6.0; validação local e CI | Concluído |
| Apply local, inspect e plan posterior | WSL2: 2 criados, inspeções e plan exit 0 | Concluído |
| Apply e limpeza efêmeros no CI | 2 criados; plan sem alterações; 2 removidos no runner | Concluído |
| Evidência CI aprovado e tag fase-1 | Tag no commit 30b49c5 aprovado, sem mover referência | Concluído |
| Proteção de main | Checks exigidos, sem force-push/exclusão; exceção admin documentada | Concluído |
| Documento no template e PDF | Versões finais com links, métricas e capturas reais; validação dos slides | Concluído |

## Escopo

Não há requisito obrigatório da fase 1 pendente. CD, imagem da API, Compose da
aplicação, Prometheus e demais funcionalidades da fase 2 serão desenvolvidos
posteriormente. Docker Engine instalado e rede/volume provisionados pertencem
à preparação da infraestrutura da fase 1.

[Execução aprovada](https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42485447573) · [Tag fase-1](https://github.com/Luiz-mnt/devops-taskflow/tree/fase-1) ·
[Resumo verificável](evidencias/resumo.json) · [Rastreabilidade](evidencias/fase1-github.md).
