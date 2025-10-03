#!/bin/bash
echo "🧹 Limpiando .env y asegurando .gitignore..."

# Asegurarnos de que exista un .gitignore y que contenga .env
if [ ! -f .gitignore ]; then
  echo ".gitignore no existe, creando uno..."
  echo ".env" > .gitignore
else
  if ! grep -q "^.env$" .gitignore; then
    echo ".env" >> .gitignore
    echo "Añadido '.env' a .gitignore ✅"
  fi
fi

# Eliminar cualquier .env del historial del stage
git rm --cached -f .env* 2>/dev/null

# Commit de limpieza
git add .gitignore
git commit -m "chore: remove .env files and update .gitignore" || echo "Nada que commitear"

# Push a la rama actual
branch=$(git rev-parse --abbrev-ref HEAD)
echo "📤 Haciendo push a la rama: $branch ..."
git push origin "$branch"

echo "✅ Limpieza completada. Archivos .env protegidos."
