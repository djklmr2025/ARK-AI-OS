#!/bin/bash
set -e

echo "🚀 Iniciando limpieza extrema de secretos y .env en el historial..."

# Verificar si git-filter-repo está instalado
if ! command -v git-filter-repo &> /dev/null
then
    echo "❌ git-filter-repo no está instalado."
    echo "👉 Instálalo con: pip install git-filter-repo"
    exit 1
fi

# Eliminar .env y similares del historial
git filter-repo --path .env --path-glob '*.env' --invert-paths

# Optimizar
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Forzar push al remoto
git push origin --force --all
git push origin --force --tags

echo "✅ Limpieza completada. Todos los .env fueron eliminados del historial."
echo "⚠️ Recuerda: cambia cualquier token/clave secreta que ya haya sido expuesta."
