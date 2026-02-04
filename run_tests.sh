#!/bin/bash
# Script para executar os testes
# Linux/Mac

echo "🧪 Executando testes da API Star Wars..."
echo ""

# Verifica se o pytest está instalado
if ! python -m pytest --version &> /dev/null; then
    echo "❌ pytest não encontrado. Instalando dependências..."
    pip install -r requirements.txt
    echo ""
fi

# Executa os testes com cobertura
echo "📊 Executando testes com relatório de cobertura..."
python -m pytest -v --cov=app --cov-report=term-missing --cov-report=html

echo ""
if [ $? -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
    echo ""
    echo "📈 Relatório de cobertura HTML gerado em: htmlcov/index.html"
    echo "   Para visualizar: open htmlcov/index.html (Mac) ou xdg-open htmlcov/index.html (Linux)"
else
    echo "❌ Alguns testes falharam. Verifique os logs acima."
fi
