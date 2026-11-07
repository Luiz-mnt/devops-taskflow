# Terraform — estado da preparação

Terraform **1.17.1**, provider **kreuzwerker/docker 4.6.0**. Foram executados com
sucesso `fmt -check -recursive`, `init -backend=false`, geração real de
`.terraform.lock.hcl` para `windows_amd64` e `linux_amd64`, `validate` e novo
`init -lockfile=readonly`. O workflow passou no actionlint **1.7.12**.

Registro: [validação local](logs/terraform-validacao.log).

O código provisiona uma rede bridge e um volume, com prefixo `taskflow` por padrão.
Não há containers ou instâncias de nuvem nesta fase. O estado e o plano são locais
e excluídos do Git. Terraform é o único dono desses dois recursos.

O daemon Docker local está em configuração no Ubuntu WSL2 exclusivo do laboratório.
Ainda não há declaração de apply local concluído nesta versão do registro.
O CI também demonstrará provisionamento efêmero, separado do laboratório local.
Resultados finais serão registrados após execução real.
