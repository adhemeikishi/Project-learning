<#
run_tests.ps1 - Automatise la configuration et l'exécution des tests sur Windows PowerShell.
Usage: Exécuter depuis le dossier du projet:
    .\scripts\run_tests.ps1
Ce script:
 - vérifie la présence de python
 - crée un venv .venv s'il n'existe pas
 - active le venv
 - installe les dépendances de requirements.txt
 - exécute les tests (tests/test_pipeline.py)
#>

# Vérifier que python est disponible
try {
    $py = Get-Command python -ErrorAction Stop
} catch {
    Write-Error "Python n'est pas disponible dans le PATH. Installez Python 3.10+ et cochez 'Add Python to PATH'."
    exit 1
}

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $projectRoot

$venvPath = Join-Path $projectRoot ".venv"
if (-Not (Test-Path $venvPath)) {
    Write-Host "Création de l'environnement virtuel .venv..."
    python -m venv $venvPath
}

# Pour éviter blocage d'exécution de scripts PowerShell
# l'utilisateur peut avoir besoin d'exécuter: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    Write-Host "Activation du venv..."
    & $activateScript
} else {
    Write-Error "Activation impossible: $activateScript introuvable"
    exit 1
}

Write-Host "Mise à jour de pip et installation des dépendances..."
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Lancement des tests unitaires..."
python -m tests.test_pipeline

if ($LASTEXITCODE -eq 0) {
    Write-Host "Tests terminés: OK ✅"
} else {
    Write-Error "Tests échoués (exit code: $LASTEXITCODE)"
    exit $LASTEXITCODE
}