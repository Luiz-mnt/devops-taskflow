# CI do PR corrigido — 08/11/2026

Execução: https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42511228720
Head do PR: b5cc28f0fc3538779ac3f432d2c4c5aaf548619d.

Qualidade/testes, Terraform e build/scan aprovados. **38 testes, zero falhas,
erros ou skips, 100% de linhas (131/131) e branches (8/8)**. O pytest registrou
1,29 s; o JUnit registrou 1,305 s. Runner Linux/Python 3.12.16.

Pip-audit: 50 pacotes Linux, zero vulnerabilidades identificadas. A medição
Windows contou 51 por incluir colorama, condicionado à plataforma.
Trivy: zero HIGH/CRITICAL corrigíveis; 40 HIGH e 2 CRITICAL sem correção.
Os relatórios integrais estão nas subpastas testes/ e security/.

As imagens do PR não foram publicadas. Provisionamento efêmero, publicação e
deploy foram corretamente omitidos nesse evento. A publicação/CD em main
aguarda a integração autorizada. A execução de PR usa a referência de merge do
GitHub; os artefatos registram essa referência e o workflow mantém o vínculo
com o head do PR nos metadados da execução.
