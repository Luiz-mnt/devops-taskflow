param()
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerCmd) {
    throw 'Docker nao encontrado. Instale/abra Docker Desktop com backend Linux; consulte docs/ambiente.md.'
}
$terraformCmd = Get-Command terraform -ErrorAction SilentlyContinue
$terraformExe = if ($terraformCmd) { $terraformCmd.Source } else {
    Join-Path (Split-Path -Parent $projectRoot) '.tools/terraform/terraform.exe'
}
if (-not (Test-Path -LiteralPath $terraformExe)) {
    throw 'Terraform nao encontrado. Instale a versao fixada em infra/versions.tf e execute novamente.'
}
$evidenceDir = Join-Path $projectRoot 'docs/evidencias/local'
New-Item -ItemType Directory -Path $evidenceDir -Force | Out-Null

function Invoke-Recorded {
    param([string]$Executable, [string[]]$Arguments, [string]$LogName)
    & $Executable @Arguments 2>&1 | Tee-Object -FilePath (Join-Path $evidenceDir $LogName)
    if ($LASTEXITCODE -ne 0) { throw "Falha no comando $Executable (exit $LASTEXITCODE). Consulte $LogName." }
}

Invoke-Recorded $dockerCmd.Source @('version') 'docker-version.txt'
$osType = & $dockerCmd.Source info --format '{{.OSType}}'
if ($LASTEXITCODE -ne 0 -or $osType.Trim() -ne 'linux') {
    throw 'Este laboratorio requer Docker Engine com Linux containers.'
}
$endpoint = & $dockerCmd.Source context inspect --format '{{.Endpoints.docker.Host}}'
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($endpoint)) {
    throw 'Nao foi possivel identificar o endpoint do contexto Docker ativo.'
}
$previousHost = $env:TF_VAR_docker_host
try {
    $env:TF_VAR_docker_host = $endpoint.Trim()
    Invoke-Recorded $terraformExe @('-chdir=infra','init','-lockfile=readonly','-input=false','-no-color') 'terraform-init.txt'
    Invoke-Recorded $terraformExe @('-chdir=infra','fmt','-check','-recursive') 'terraform-fmt.txt'
    Invoke-Recorded $terraformExe @('-chdir=infra','validate','-no-color') 'terraform-validate.txt'
    Invoke-Recorded $terraformExe @('-chdir=infra','plan','-out=local.tfplan','-input=false','-no-color') 'terraform-plan.txt'
    Write-Host 'Revise o plano acima. A aplicacao criara apenas a rede e o volume deste laboratorio.'
    if ((Read-Host 'Digite APLICAR para confirmar o plano') -cne 'APLICAR') {
        throw 'Plano nao aplicado: confirmacao nao fornecida.'
    }
    Invoke-Recorded $terraformExe @('-chdir=infra','apply','-input=false','-no-color','local.tfplan') 'terraform-apply.txt'
    Invoke-Recorded $dockerCmd.Source @('network','inspect','taskflow-net') 'network.json'
    Invoke-Recorded $dockerCmd.Source @('volume','inspect','taskflow-data') 'volume.json'
    Invoke-Recorded $terraformExe @('-chdir=infra','plan','-detailed-exitcode','-input=false','-no-color') 'terraform-plan-after.txt'
    [ordered]@{
        timestamp = [DateTimeOffset]::UtcNow.ToString('o')
        result = 'apply e inspecoes aprovados; plan posterior exit 0'
        resources = @('taskflow-net','taskflow-data')
        local = $true
    } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $evidenceDir 'resultado.json') -Encoding UTF8
    Write-Host 'Provisionamento local comprovado. Logs em docs/evidencias/local; atualize o relatorio de entrega.'
} finally {
    $env:TF_VAR_docker_host = $previousHost
}
