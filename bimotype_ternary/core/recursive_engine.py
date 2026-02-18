import os
import uuid
import hashlib
import time
import math
import platform
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

# Database integration
from ..database.manager import DatabaseManager

@dataclass
class HardwareMetrics:
    """Static hardware identifiers for the fingerprint."""
    node: str = platform.node()
    system: str = platform.system()
    machine: str = platform.machine()
    cpu_count: int = os.cpu_count() or 0
    hw_uuid: str = str(uuid.getnode()) # MAC address based UUID
    
    def to_hash_input(self) -> str:
        return f"{self.node}-{self.system}-{self.machine}-{self.cpu_count}-{self.hw_uuid}"

class RecursiveEngine:
    """
    Engine that manages recursive information processing and 
    hardware-based session fingerprinting using Metriplectic principles.
    En esta versión MVP, la persistencia se realiza en una DB SQLite.
    """
    
    PHI = (1 + math.sqrt(5)) / 2 # Golden Ratio
    
    def __init__(self, db_path: str = "bimotype.sqlite3"):
        self.db = DatabaseManager(db_path)
        self.hw_metrics = HardwareMetrics()
        
    def generate_fingerprint(self, session_n: int) -> str:
        """
        Generates a hardware fingerprint modulated by the Golden Operator O_n.
        Rule 2.1: O_n = cos(pi n) * cos(pi phi n)
        """
        # Calculate O_n modulation
        o_n = math.cos(math.pi * session_n) * math.cos(math.pi * self.PHI * session_n)
        
        # Combine hardware metrics with modulation
        raw_input = self.hw_metrics.to_hash_input()
        input_with_modulation = f"{raw_input}-On:{o_n:.10f}-S:{session_n}"
        
        fingerprint = hashlib.sha256(input_with_modulation.encode()).hexdigest()
        
        # Guardar registro de identidad en DB
        self.db.record_identity(fingerprint, asdict(self.hw_metrics), o_n)
        
        return fingerprint

    def load_previous_feedback(self) -> Dict[str, Any]:
        """Loads state from the previous processing cycle from the DB."""
        payload = self.db.get_latest_state()
        return {"data": payload} if payload else {}

    def save_current_feedback(self, data: Dict[str, Any], session_id: str):
        """Saves data to be used in the next cycle (Recursion) in the DB."""
        # En esta implementación, session_id se usa para identificar la sesión en la DB
        # El manager se encarga de buscar por fingerprint (que es parte del session_id en el manager superior)
        # Para simplificar el MVP, usamos el fingerprint directamente si está disponible.
        # Aquí asumimos que session_id contiene el fingerprint (SESSION-n-FINGERPRINT)
        fingerprint = session_id.split('-')[-1] if '-' in session_id else session_id
        self.db.save_recursive_state(fingerprint, data)
            
    def log_audit(self, session_id: str, fingerprint: str):
        """Records the session startup for auditing in the DB."""
        # El manager se encarga de crear el SystemSession si no existe
        # session_n se extrae del session_id si es posible
        session_n = 0
        try:
            if '-' in session_id:
                session_n = int(session_id.split('-')[1])
        except:
            pass
            
        self.db.create_session_record(session_n, fingerprint)
        self.db.add_audit_log(fingerprint, "SESSION_START", f"Iniciando sesión {session_id}")

    def compute_feedback_loop(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes info by merging current input with previous cycle output.
        This closes the recursive loop.
        """
        prev_data = self.load_previous_feedback().get("data", {})
        
        # Simple recursive merge/evolution logic
        evolved_data = prev_data.copy()
        for k, v in input_data.items():
            if k in evolved_data and isinstance(v, (int, float)):
                # Metriplectic-like evolution: mix current with record
                evolved_data[k] = (evolved_data[k] * 0.7) + (v * 0.3)
            else:
                evolved_data[k] = v
        
        return evolved_data
