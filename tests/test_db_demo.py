import os
import pytest
from bimotype_ternary.core.session_manager import SessionManager
from bimotype_ternary.database.manager import DatabaseManager
from bimotype_ternary.database.models import IdentityMetrics, AuditLog

def test_db_session_lifecycle():
    """Valida el ciclo de vida de una sesión y su persistencia."""
    db_file = "test_temp.sqlite3"
    if os.path.exists(db_file):
        os.remove(db_file)
        
    try:
        sm = SessionManager(db_path=db_file)
        
        # 1. Iniciar sesión
        session_info = sm.start_session(session_number=99)
        assert session_info['session_id'].startswith("SESSION-99-")
        assert len(session_info['fingerprint']) > 0
        
        # 2. Procesar y evolucionar
        data = {"entropy": 0.5, "test": True}
        evolved = sm.process_and_evolve(data)
        assert "entropy" in evolved
        
        # 3. Verificar persistencia en DB
        db_mgr = DatabaseManager(db_file)
        session = db_mgr.get_session()
        
        # Verificar logs
        logs = session.query(AuditLog).all()
        assert len(logs) >= 1
        assert any(log.event_type == "SESSION_START" for log in logs)
        
        session.close()
    finally:
        if os.path.exists(db_file):
            os.remove(db_file)

def test_database_manager_identity():
    """Valida el registro de identidad con el Operador Áureo."""
    db_file = "test_identity.sqlite3"
    if os.path.exists(db_file):
        os.remove(db_file)
        
    try:
        db_mgr = DatabaseManager(db_file)
        fingerprint = "test_fingerprint_123"
        metrics = {"node": "test-node", "system": "test-os"}
        o_n = 1.618
        
        db_mgr.record_identity(fingerprint, metrics, o_n)
        
        session = db_mgr.get_session()
        identity = session.query(IdentityMetrics).filter_by(fingerprint=fingerprint).first()
        
        assert identity is not None
        assert identity.node_name == "test-node"
        assert identity.o_n_parameter == 1.618
        
        session.close()
    finally:
        if os.path.exists(db_file):
            os.remove(db_file)
