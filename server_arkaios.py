
# server_arkaios.py — ARKAIOS server (UI split + auth hotfix + endpoints)
import os, json, base64, uuid, time, logging
from datetime import datetime
from pathlib import Path
from threading import Thread, Event

from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS

# --- Lógica de Negocio de ARKAIOS ---
import arkaios_logic

# --- (Opcional) Google token verification ---
try:
    from google.oauth2 import id_token
    from google.auth.transport import requests as grequests
    HAVE_GOOGLE = True
except Exception:
    HAVE_GOOGLE = False

# ========== CONFIG ==========
APP_DIR = Path(__file__).parent.resolve()
STATIC_DIR = APP_DIR
STORAGE = Path(os.getenv("ARK_STORAGE", "data")).resolve()
MEM_DIR = Path(os.getenv("MEMORY_DIR", str(STORAGE / "memory"))).resolve()

LOG_PATH = MEM_DIR / "arkaios_log.jsonl"
SESSION_PATH = MEM_DIR / "arkaios_session_last.json"
TASKS_PATH = MEM_DIR / "tasks.json"
DOCS_PATH = MEM_DIR / "docs.html"

STORAGE.mkdir(parents=True, exist_ok=True)
MEM_DIR.mkdir(parents=True, exist_ok=True)

# ========== LOGGING ==========
logger = logging.getLogger("arkaios")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
logger.addHandler(ch)

def log_json(event: dict):
    try:
        event.setdefault("ts", int(time.time() * 1000))
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.warning(f"No se pudo escribir log JSONL: {e}")

# ========== APP ==========
app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")
CORS(app, resources={r"/*": {"origins": "*"}})
SESSIONS = {}  # token -> {"email":..., "name":..., "iat":...}

# ===== Util =====
def ok(data=None, **kw):
    obj = {"ok": True}
    if isinstance(data, dict):
        obj.update(data)
    if kw:
        obj.update(kw)
    return jsonify(obj)

def err(msg, code=400, **kw):
    payload = {"ok": False, "error": str(msg)}
    payload.update(kw)
    log_json({"type": "error", "message": str(msg)})
    return jsonify(payload), code

# ====== Front estático ======
@app.get("/")
def home():
    return send_from_directory(STATIC_DIR, "index.html")

@app.get("/app")
def app_page():
    return send_from_directory(STATIC_DIR, "arkaios-integrated.html")

# ====== Health Check ======
@app.get("/health")
def health():
    return ok(name="ARKAIOS Server", status="ready")

# ====== Autenticación ======
@app.post("/auth/google")
def auth_google():
    # ... (sin cambios en la lógica de autenticación)
    body = request.get_json(force=True) or {}
    email = "demo@arkaios.local"
    name = "Demo User"
    tok = uuid.uuid4().hex
    SESSIONS[tok] = {"email": email, "name": name, "iat": int(time.time())}
    log_json({"type": "login", "email": email})
    return ok(token=tok, user={"email": email, "name": name})

# ====== ARKAIOS CORE API ======

@app.post("/api/accounts/create")
def api_create_account():
    try:
        body = request.get_json(force=True) or {}
        nombre = body.get('nombre')
        usuario = body.get('usuario')
        saldo = body.get('saldo', 0)
        account_data = arkaios_logic.create_account(nombre, usuario, saldo)
        log_json({"type": "account_create", "usuario": usuario})
        return ok(account=account_data)
    except (ValueError, FileExistsError) as e:
        return err(str(e))
    except Exception as e:
        logger.error(f"Error en create_account: {e}")
        return err("Error interno del servidor al crear la cuenta.", 500)

@app.post("/api/operations/transfer")
def api_transfer():
    try:
        body = request.get_json(force=True) or {}
        origen = body.get('origen_usuario')
        destino = body.get('destino_usuario')
        monto = body.get('monto')
        arkaios_logic.transferir(origen, destino, monto)
        log_json({"type": "transfer", "from": origen, "to": destino, "amount": monto})
        return ok(message="Transferencia completada exitosamente.")
    except (ValueError, FileNotFoundError) as e:
        return err(str(e))
    except Exception as e:
        logger.error(f"Error en transfer: {e}")
        return err("Error interno del servidor durante la transferencia.", 500)

@app.post("/api/operations/redeem")
def api_redeem_code():
    try:
        body = request.get_json(force=True) or {}
        usuario = body.get('usuario')
        code = body.get('code')
        valor = arkaios_logic.redeem_code(usuario, code)
        log_json({"type": "redeem_code", "user": usuario, "code": code, "value": valor})
        return ok(message=f"Código canjeado exitosamente por un valor de {valor}.", value=valor)
    except ValueError as e:
        return err(str(e))
    except Exception as e:
        logger.error(f"Error en redeem_code: {e}")
        return err("Error interno del servidor al canjear el código.", 500)

@app.post("/api/codes/generate")
def api_generate_codes():
    try:
        body = request.get_json(force=True) or {}
        cantidad = int(body.get('cantidad', 1))
        valor = float(body.get('valor', 0))
        dias_expiracion = body.get('dias_expiracion')
        if dias_expiracion is not None:
            dias_expiracion = int(dias_expiracion)
        
        nuevos_codigos = arkaios_logic.generate_new_codes(cantidad, valor, dias_expiracion)
        log_json({"type": "generate_codes", "count": cantidad, "value": valor})
        return ok(codes=nuevos_codigos)
    except (ValueError, TypeError) as e:
        return err(str(e))
    except Exception as e:
        logger.error(f"Error en generate_codes: {e}")
        return err("Error interno del servidor al generar códigos.", 500)

# --- (El resto de los endpoints de la API original como /chat, /files, etc. permanecen igual) ---

# ... (Aquí iría el resto del código de server_arkaios.py sin modificar)
# ... (Por brevedad, se omite el código que no ha cambiado)

# ====== Chat (placeholder) ======
@app.post("/chat")
def chat():
    body = request.get_json(force=True) or {}
    msg = (body.get("message") or "").strip()
    # La IA de ARKAIOS debería procesar el mensaje aquí y llamar a la API si es necesario
    # Por ahora, es un simple eco.
    logger.debug(f"/chat message: {msg!r}")
    log_json({"type": "chat", "message": msg})
    reply = f"Recibí tu mensaje: '{msg}'. La lógica de ARKAIOS ahora reside en el backend."
    return ok(reply=reply)

# ====== Archivos ======
@app.get("/files")
def list_files():
    items = []
    # No mostrar los códigos generados en la lista de archivos por seguridad.
    for p in STORAGE.glob("**/*"):
        if p.is_file() and p.name != 'codes.json':
            items.append(str(p.relative_to(STORAGE)))
    return ok(files=items)

@app.post("/save")
def save_file():
    body = request.get_json(force=True) or {}
    name = (body.get("name") or "").strip()
    content = body.get("content") or ""
    if not name or name == 'codes.json': # Prohibir sobreescribir la DB de códigos
        return err("Nombre de archivo no válido o prohibido.")
    
    path = STORAGE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    log_json({"type": "file_save", "name": name, "size": len(content)})
    return ok()

# ... (Resto de endpoints sin cambios significativos)


# ====== Main ======
if __name__ == "__main__":
    logger.info("🚀 Servidor ARKAIOS iniciando…")
    logger.info(f"📂 STORAGE: {STORAGE}")
    logger.info(f"🧠 MEM_DIR: {MEM_DIR}")
    logger.info("🔗 Endpoints de ARKAIOS Core API listos.")
    logger.info("🌐 UI: http://127.0.0.1:5000/")

    try:
        # Usar use_reloader=False para evitar que el script se ejecute dos veces en debug mode
        app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
    finally:
        # Lógica de apagado si fuera necesaria
        logger.info("Servidor ARKAIOS detenido.")

