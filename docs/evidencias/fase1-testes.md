# Testes automatizados — evidências reais

Execução local em 06/11/2026 (America/Sao_Paulo), registrada em
2026-11-07T00:46:26Z. Ambiente **CPython 3.12.16**, Windows, pytest 9.2.0.

| Verificação | Resultado observado |
|---|---|
| Ruff check | Aprovado, exit 0 |
| Ruff format --check | Aprovado, 13 arquivos já formatados, exit 0 |
| pytest | **32 aprovados**, 0 falhas, 1 aviso, **2,86 s** |
| Cobertura de linhas | **100%**, 89 instruções, 0 ausentes |
| Cobertura de branches | **100%**, 4 branches, 0 ausentes |
| Gate de cobertura | Mínimo 80% atingido, sem reduzir a exigência |

Comandos na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
```

Nesta sessão isolada, o diretório temporário padrão do Windows não permitia a
criação de arquivos pelo pytest. A execução medida usou `--basetemp` em um
diretório novo sob a pasta de trabalho e `-o cache_dir=...`; os caminhos exatos
constam no [registro integral](logs/python312-testes.log). Isso não modifica os
testes nem a exigência de cobertura. No runner Linux o comando é `python -m pytest`.

Os testes verificam criação, título obrigatório, trim/espaços, tamanho, tipos,
campos extras, NUL, listagem, conclusão idempotente, entradas de status inválidas,
ID inexistente/inválido/fora do limite SQLite, tratamento literal de SQL,
persistência entre instâncias, isolamento de bancos e saúde com banco acessível
ou corrompido/tabela ausente. Cada caso usa banco temporário.

Os relatórios gerados ficam em `reports/junit.xml`, `reports/coverage.xml` e
`reports/htmlcov/`; são artefatos do CI e não caches versionados. A evidência
remota identifica seu próprio commit e duração em `fase1-github.md`/`resumo.json`.
O tempo local não é apresentado como tempo do runner.

O único aviso é `StarletteDeprecationWarning`: a biblioteca sinaliza futura
migração de `httpx` para `httpx2`. A versão fixada funciona e todos os testes
passaram; o aviso permanece visível, sem supressão.

Resolução de versões: [log de dependências](logs/dependencias.log).
