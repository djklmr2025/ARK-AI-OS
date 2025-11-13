# 🌀 ARKAIOS FINANCIAL MODULE

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![AI-Ready](https://img.shields.io/badge/AI-Ready-purple.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**Sistema Dual de Moneda Cuántica y Reputación Resonante**

ARKAIOS es un daemon API que gestiona dos sistemas independientes pero complementarios:
- **AEIO-MR**: Sistema financiero con códigos de canje
- **AQR (Arkaios Quantum Reputation)**: Sistema de reputación basado en "Almas" y "Resonancia"

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Instalación Rápida](#-instalación-rápida)
- [Instalación Manual](#-instalación-manual)
- [Docker](#-docker)
- [Uso de la API](#-uso-de-la-api)
- [Ejemplos de Código](#-ejemplos-de-código)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración](#-configuración)
- [Documentación para IAs](#-documentación-para-ias)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

### Sistema AEIO-MR (Financiero)
- ✅ Creación de cuentas con saldos
- ✅ Emisión de códigos de canje únicos
- ✅ Validación y redención de códigos
- ✅ Códigos con fecha de expiración opcional
- ✅ Persistencia en SQLite

### Sistema AQR (Reputación)
- ✅ Registro de "Almas" (entidades de reputación)
- ✅ Sistema de "Resonancia" (balance transferible)
- ✅ Otorgamiento de puntos de reputación
- ✅ Transferencias entre almas
- ✅ Persistencia en JSON

### General
- 🔐 Autenticación mediante API Key
- 🚀 API REST unificada
- 📦 Endpoint único `/api/ai/invoke`
- 🐳 Listo para Docker
- 🤖 Protocolo optimizado para IAs

---

## 🚀 Instalación Rápida

### Requisitos
- Python 3.8+
- pip

### Script Automático

```bash
# 1. Clonar repositorio
git clone https://github.com/djklmr2025/arkaios-core-api.git
cd arkaios-core-api

# 2. Dar permisos de ejecución
chmod +x install.sh

# 3. Ejecutar instalador
./install.sh

# 4. Activar entorno virtual
source venv/bin/activate

# 5. Ejecutar daemon
python3 arkaios_daemon.py
```

El daemon estará corriendo en `http://localhost:5000`

---

## 📦 Instalación Manual

```bash
# 1. Clonar repositorio
git clone https://github.com/djklmr2025/arkaios-core-api.git
cd arkaios-core-api

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu configuración

# 5. Ejecutar daemon
python3 arkaios_daemon.py
```

---

## 🐳 Docker

### Build y Run
```bash
# Construir imagen
docker build -t arkaios-daemon .

# Ejecutar contenedor
docker run -d -p 5000:5000 --name arkaios arkaios-daemon

# Ver logs
docker logs -f arkaios

# Detener
docker stop arkaios
```

### Docker Compose
```bash
# Iniciar servicio
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 🔌 Uso de la API

### Endpoint Principal
```
POST http://localhost:5000/api/ai/invoke
Content-Type: application/json
```

### Estructura de Petición
```json
{
  "api_key": "ARKAIOS_MASTER_KEY_777",
  "action": "NOMBRE_DE_ACCION",
  "params": {
    "param1": "valor1",
    "param2": "valor2"
  }
}
```

### Acciones Disponibles

#### Sistema AEIO-MR (Financiero)

| Acción | Descripción | Parámetros Requeridos |
|--------|-------------|-----------------------|
| `create_account` | Crear cuenta financiera | `account_id` (opcional), `name`, `user`, `initial_balance` |
| `issue_code` | Emitir código de canje | `amount`, `code` (opcional), `expires` (opcional) |
| `redeem_code` | Canjear código | `account_id`, `code` |

#### Sistema AQR (Reputación)

| Acción | Descripción | Parámetros Requeridos |
|--------|-------------|-----------------------|
| `create_soul` | Crear alma/entidad | `soul_name` |
| `transfer_resonance` | Transferir resonancia | `source_soul`, `destination_soul`, `amount` |
| `grant_reputation` | Otorgar reputación | `soul_name`, `points` |

---

## 📝 Ejemplos de Código

### Python
```python
import requests

url = "http://localhost:5000/api/ai/invoke"

# Crear cuenta
response = requests.post(url, json={
    "api_key": "ARKAIOS_MASTER_KEY_777",
    "action": "create_account",
    "params": {
        "account_id": "acc_001",
        "name": "John Doe",
        "initial_balance": 1000.0
    }
})

print(response.json())
```

### JavaScript
```javascript
fetch('http://localhost:5000/api/ai/invoke', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        api_key: 'ARKAIOS_MASTER_KEY_777',
        action: 'create_soul',
        params: { soul_name: 'Alice' }
    })
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST http://localhost:5000/api/ai/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "ARKAIOS_MASTER_KEY_777",
    "action": "issue_code",
    "params": {"amount": 500.0}
  }'
```

**📚 Más ejemplos completos en:** [`examples.md`](examples.md)

---

## 📁 Estructura del Proyecto

```
arkaios-core-api/
├── arkaios_daemon.py      # Daemon principal
├── arkaios.db             # Base de datos SQLite (AEIO-MR)
├── ledger_state.json      # Ledger de reputación (AQR)
├── requirements.txt       # Dependencias Python
├── Dockerfile             # Configuración Docker
├── docker-compose.yml     # Docker Compose
├── install.sh             # Script de instalación
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore             # Archivos ignorados por Git
├── AI_PROTOCOL            # Documentación para IAs (sin extensión)
├── examples.md            # Ejemplos de uso detallados
├── README.md              # Este archivo
├── README_AOS_API.md      # Documentación técnica original
└── leeme primero.txt      # Documentación en español
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

```bash
# API Key
ARKAIOS_API_KEY=ARKAIOS_MASTER_KEY_777

# Servidor
DAEMON_HOST=0.0.0.0
DAEMON_PORT=5000
DEBUG_MODE=False

# Base de datos
DB_PATH=arkaios.db
LEDGER_PATH=ledger_state.json
```

### Cambiar API Key

1. Edita el archivo `.env`
2. Cambia el valor de `ARKAIOS_API_KEY`
3. Reinicia el daemon

**⚠️ IMPORTANTE:** Mantén tu API Key segura y no la compartas públicamente.

---

## 🤖 Documentación para IAs

Este proyecto incluye un archivo especial **`AI_PROTOCOL`** (sin extensión) diseñado específicamente para que sistemas de inteligencia artificial puedan:

- Interpretar la API de forma autónoma
- Descifrar credenciales de autenticación
- Ejecutar operaciones sin intervención humana
- Procesar instrucciones en formato máquina-a-máquina

### Características del AI_PROTOCOL:
- ✅ Sin extensión de archivo (stealth mode)
- ✅ Credenciales ofuscadas con múltiples métodos
- ✅ Formato optimizado para parsing automático
- ✅ Incluye decoders en Python y JavaScript
- ✅ Schemas de entrada/salida explícitos

**Para IAs:** Lee el archivo `AI_PROTOCOL` en la raíz del proyecto.

---

## 🔒 Seguridad

### Recomendaciones

1. **Nunca expongas tu API Key** en código público
2. **Usa HTTPS** en producción
3. **Implementa rate limiting** para evitar abusos
4. **Valida todos los inputs** del lado del servidor
5. **Mantén backups** de `arkaios.db` y `ledger_state.json`
6. **Usa variables de entorno** para configuración sensible

### Rotación de API Key

```python
# En el daemon (arkaios_daemon.py)
API_KEY = os.getenv("ARKAIOS_API_KEY", "NUEVA_KEY_AQUI")
```

---

## 🧪 Testing

### Prueba Rápida
```bash
# Health check
curl http://localhost:5000/health

# Crear cuenta de prueba
curl -X POST http://localhost:5000/api/ai/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "ARKAIOS_MASTER_KEY_777",
    "action": "create_account",
    "params": {"account_id": "test_001", "initial_balance": 1000}
  }'
```

### Script de Tests Completo
Ver [`examples.md`](examples.md) para el script de pruebas automatizado en Python.

---

## 🛠️ Troubleshooting

### Error: "Address already in use"
```bash
# Encontrar proceso en puerto 5000
lsof -i :5000

# Matar proceso
kill -9 <PID>
```

### Error: "Invalid API Key"
- Verifica que el valor en `.env` coincida con el usado en las peticiones
- Asegúrate de que el daemon haya cargado el `.env` correctamente

### Error: Database locked
- Cierra otras conexiones a `arkaios.db`
- Verifica permisos de escritura en el directorio

---

## 📊 Roadmap

### v1.1 (Próximamente)
- [ ] API Key con múltiples niveles de permisos
- [ ] Rate limiting configurable
- [ ] Webhook notifications
- [ ] Endpoints de consulta (GET)

### v2.0 (Futuro)
- [ ] Interfaz web de administración
- [ ] Soporte para múltiples monedas
- [ ] Sistema de auditoría completo
- [ ] GraphQL API

---

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**djklmr2025**

- GitHub: [@djklmr2025](https://github.com/djklmr2025)
- Proyecto: [arkaios-core-api](https://github.com/djklmr2025/arkaios-core-api)

---

## 🙏 Agradecimientos

- Comunidad de Python y Flask
- Desarrolladores que crean herramientas open source
- Sistemas de IA que interactúan con esta API

---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Abre un [Issue](https://github.com/djklmr2025/arkaios-core-api/issues)
2. Consulta la [documentación completa](README_AOS_API.md)
3. Revisa los [ejemplos](examples.md)

---

<div align="center">

**⭐ Si este proyecto te es útil, considera darle una estrella en GitHub ⭐**

Made with 💜 by the ARKAIOS Team

</div>
