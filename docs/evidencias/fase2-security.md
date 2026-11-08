# Segurança da fase 2 — evidência local

Em 08/11/2026, pip-audit 2.10.1 avaliou as dependências de produção e
desenvolvimento fixadas: 51 pacotes, zero vulnerabilidades identificadas,
exit 0, sem exclusões. O inventário está em
[pip-audit-local.json](fase2-local/security/pip-audit-local.json).

Trivy 0.76.2 analisou a imagem local inicial, Debian 12.15/Python 3.12.16,
incluindo pacotes do sistema e Python. O Config ID independente, calculado
pelos bytes da configuração no docker-save, foi
`sha256:cc95a9a65754045b2b6f54614d96a79acbb98808c58d3a094cf80749089da2b4`.
O Docker local 29 usa um OCI index como inspect.Id; essa representação não
deve ser comparada diretamente ao Config ID retornado pelo Trivy.

Resultado real: **0 HIGH/CRITICAL com correção disponível**, **40 HIGH e
2 CRITICAL sem correção informada**, 122 MEDIUM e 109 LOW. O gate bloqueia os
HIGH/CRITICAL corrigíveis, conforme a política do guia. O inventário completo
é preservado, sem ocultar os demais achados ou alegar ausência de risco.

[Inventário completo](fase2-local/security/trivy-local.json) ·
[Resultado do gate](fase2-local/security/image-security-local.json).

São resultados locais da imagem inicial, anteriores à publicação. As provas
remotas deverão manter seu próprio commit, imagem por digest e data de scan.
O pipeline valida checksum e Config ID do arquivo efetivamente analisado;
depois confere novamente a imagem carregada e a baixada do registry, sem rebuild.

Mitigações presentes: execução sem root, filesystem raiz somente leitura,
capabilities removidas, no-new-privileges, portas em loopback e nenhum socket
Docker nos containers. Essas medidas reduzem a exposição do laboratório, mas
não eliminam as vulnerabilidades registradas. Acompanhar novas bases e scans
é uma melhoria contínua necessária. Não há exceção ampla de CVEs ou falhas.
