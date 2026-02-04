# Script para executar os testes
# Windows PowerShell

Write-Host "🧪 Executando testes da API Star Wars..." -ForegroundColor Cyan
Write-Host ""

# Verifica se o pytest está instalado
$pytestInstalled = python -m pytest --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ pytest não encontrado. Instalando dependências..." -ForegroundColor Red
    pip install -r requirements.txt
    Write-Host ""
}

# Executa os testes com cobertura
Write-Host "📊 Executando testes com relatório de cobertura..." -ForegroundColor Yellow
python -m pytest -v --cov=app --cov-report=term-missing --cov-report=html

Write-Host ""
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Todos os testes passaram!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📈 Relatório de cobertura HTML gerado em: htmlcov/index.html" -ForegroundColor Cyan
    Write-Host "   Para visualizar: " -NoNewline
    Write-Host "start htmlcov/index.html" -ForegroundColor White
} else {
    Write-Host "❌ Alguns testes falharam. Verifique os logs acima." -ForegroundColor Red
}
