import json
from bimotype_ternary.core.session_manager import SessionManager
from bimotype_ternary.database.manager import DatabaseManager

def run_db_demo():
    print(f"\n{'='*60}")
    print(f"DATABASE & RECURSION DEMO")
    print(f"{'='*60}")
    
    # Usar una base de datos específica para el demo
    db_file = "demo_mvp.sqlite3"
    sm = SessionManager(db_path=db_file)
    
    # 1. Simular una sesión
    iteration = 1
    print(f"\n--- Iniciando Sesión {iteration} ---")
    session_info = sm.start_session(session_number=iteration)
    print(f"Session ID:  {session_info['session_id']}")
    print(f"Fingerprint: {session_info['fingerprint'][:24]}...")
    
    # Evolucionar datos
    new_data = {"entropy": 0.88, "system_health": 100}
    evolved = sm.process_and_evolve(new_data)
    print(f"Estado Guardado en DB: {evolved}")

    # 2. Consultar directamente la Base de Datos para auditoría
    print("\n--- Consulta de Auditoría (Directo desde DB) ---")
    db_mgr = DatabaseManager(db_file)
    session = db_mgr.get_session()
    
    from bimotype_ternary.database.models import IdentityMetrics, AuditLog

    # Ver identidad
    identity = session.query(IdentityMetrics).first()
    if identity:
        print(f"Identidad Detectada: {identity.node_name} ({identity.system_os})")
        print(f"Parámetro O_n: {identity.o_n_parameter}")
    
    # Ver logs
    logs = session.query(AuditLog).all()
    print(f"\nLogs de Auditoría encontrados: {len(logs)}")
    for log in logs:
        print(f"  [{log.timestamp}] {log.event_type}: {log.description}")
    
    session.close()
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_db_demo()
