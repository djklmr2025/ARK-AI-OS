"""
Ledger Manager for ETHORA
Persiste el ReputationLedger a un archivo JSON.
Diseñado por ELEMIA.
"""

import json
from datetime import datetime
from ethora_reputation_protocol import ReputationLedger, Contribution, Resonance

LEDGER_FILE = "ledger.json"

def save_ledger(ledger: ReputationLedger):
    """Guarda el estado del ReputationLedger en ledger.json."""
    
    def default_serializer(o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, (Contribution, Resonance)):
            return o.__dict__
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

    ledger_repr = {
        'souls': ledger.souls,
        'contributions': list(ledger.contributions.values())
    }

    with open(LEDGER_FILE, 'w', encoding='utf-8') as f:
        json.dump(ledger_repr, f, default=default_serializer, indent=4)
    print(f"Ledger guardado en {LEDGER_FILE}")


def load_ledger() -> ReputationLedger:
    """Carga el ReputationLedger desde ledger.json.""""""
    try:
        with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        ledger = ReputationLedger()
        ledger.souls = data.get('souls', {})

        for c_data in data.get('contributions', []):
            c_data['timestamp'] = datetime.fromisoformat(c_data['timestamp'])
            
            resonances_data = c_data.get('resonances', [])
            for r_data in resonances_data:
                r_data['timestamp'] = datetime.fromisoformat(r_data['timestamp'])
            
            c_data['resonances'] = [Resonance(**r) for r in resonances_data]
            
            contribution = Contribution(**c_data)
            
            ledger.contributions[contribution.contribution_id] = contribution
        
        print(f"Ledger cargado desde {LEDGER_FILE}")
        return ledger
        
    except FileNotFoundError:
        print(f"No se encontró {LEDGER_FILE}. Creando un nuevo Ledger.")
        return ReputationLedger()
    except Exception as e:
        print(f"Error al cargar el ledger ({e.__class__.__name__}: {e}). Creando uno nuevo.")
        return ReputationLedger()
