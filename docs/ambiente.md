# Ambiente observado

Data da preparação: **06/11/2026**, fuso America/Sao_Paulo.

| Item | Resultado observado |
|---|---|
| Sistema | Windows, versão NT 10.0.26200.0, 64 bits |
| Shell | Windows PowerShell 5.1.26100.9711 |
| Git | 2.46.2.windows.1 |
| GitHub CLI | 2.86.0 |
| Conta autenticada | Luiz-mnt, confirmada com `gh api user --jq .login` |
| Python original | 3.13 em C:\\Python313; usado somente no diagnóstico inicial |
| Python do projeto | CPython 3.12.16 portátil, baixado pelo uv 0.13.7; ambiente virtual `.venv` |
| Terraform | 1.17.1, binário oficial portátil; não adicionado ao PATH global |
| Provider Docker | kreuzwerker/docker 4.6.0; lock real para windows_amd64 e linux_amd64 |
| actionlint | 1.7.12, distribuição oficial portátil, workflow validado |
| Docker | Não localizado no PATH nem nos caminhos de instalação verificados; nenhum daemon disponível |
| WSL | Comando disponível; `wsl --list --verbose` confirmou ausência de distribuições instaladas |
| PowerPoint | Executável instalado; automação COM indisponível nesta sessão (80070520) |

Python, uv, Terraform e actionlint foram obtidos em `.tools/` da pasta de trabalho
que contém o repositório. Não pertencem ao código publicado. O SHA256 do ZIP
Terraform foi comparado com o checksum oficial:
`a3b71365cff94c0f978cf75d86addb075ea1bb6409055ea0ab359bf057d7898a`.

As primeiras consultas de rede no sandbox falharam com WinError10013, e a primeira
consulta de autenticação aparentou token inválido. Repetidas com acesso de rede
autorizado, confirmaram autenticação válida; não foi necessário novo login.
Tokens não foram copiados para o repositório nem para esta documentação.

## Limitação local e como resolvê-la

O código, os testes e a validação Terraform podem ser executados neste Windows.
O provisionamento **local** exige instalar/iniciar Docker com backend Linux.
Um apply bem-sucedido no GitHub Actions comprova apenas o ambiente do runner.

1. Consulte os [requisitos oficiais do Docker Desktop para Windows](https://docs.docker.com/desktop/setup/install/windows-install/).
2. Instale uma distribuição seguindo a [documentação oficial do WSL](https://learn.microsoft.com/windows/wsl/install), se usar esse backend. O comando administrativo usual é `wsl --install -d Ubuntu`; reinicie se solicitado.
3. Instale e abra Docker Desktop, selecione Linux containers e aguarde o servidor iniciar. Se usar Ubuntu/WSL, habilite a integração da distribuição.
4. No PowerShell, `docker version` deve mostrar Client **e Server**; `docker info --format '{{.OSType}}'` deve mostrar `linux`.
5. Na raiz deste repositório, execute `powershell -ExecutionPolicy Bypass -File scripts/provisionar-local.ps1`. Revise e confirme o plano exibido pelo Terraform. O script não destrói dados locais.
6. Atualize as evidências e o documento da entrega com os logs reais produzidos. A pendência local só pode ser encerrada após apply, inspect e novo plan sem alterações.

Nenhum Docker Engine, distribuição WSL ou componente de virtualização foi
instalado silenciosamente como parte desta preparação.
