import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, SystemSession, RecursiveState, IdentityMetrics, AuditLog
from typing import Dict, Any, Optional, List

class DatabaseManager:
    """
    Manager que orquesta la persistencia del sistema.
    Implementa el puente entre la teoría (models) y la práctica (disk).
    """
    
    def __init__(self, db_path: str = "bimotype.sqlite3"):
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # Crear tablas si no existen
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def create_session_record(self, session_number: int, fingerprint: str) -> SystemSession:
        """Busca o crea una entrada de sesión en la DB para evitar errores de integridad."""
        db = self.get_session()
        try:
            # Primero intentar buscar una sesión existente con el mismo fingerprint
            session = db.query(SystemSession).filter(SystemSession.fingerprint == fingerprint).first()
            
            if not session:
                # Si no existe, crearla
                session = SystemSession(
                    session_number=session_number,
                    fingerprint=fingerprint
                )
                db.add(session)
                db.commit()
                db.refresh(session)
            
            return session
        finally:
            db.close()

    def save_recursive_state(self, fingerprint: str, payload: Dict[str, Any]):
        """Guarda o actualiza el estado de información para una sesión."""
        db = self.get_session()
        try:
            session = db.query(SystemSession).filter(SystemSession.fingerprint == fingerprint).first()
            if not session:
                return # O lanzar error
            
            state = db.query(RecursiveState).filter(RecursiveState.session_id == session.id).first()
            if not state:
                state = RecursiveState(session_id=session.id, payload=payload)
                db.add(state)
            else:
                state.payload = payload
                
            db.commit()
        finally:
            db.close()

    def get_latest_state(self) -> Optional[Dict[str, Any]]:
        """Busca el estado de la última sesión exitosa."""
        db = self.get_session()
        try:
            latest_session = db.query(SystemSession).order_by(SystemSession.id.desc()).first()
            if latest_session and latest_session.state:
                return latest_session.state.payload
            return None
        finally:
            db.close()

    def record_identity(self, fingerprint: str, metrics: Dict[str, Any], o_n: float):
        """Registra el hardware y su modulación áurea."""
        db = self.get_session()
        try:
            # Evitar duplicados por fingerprint
            if db.query(IdentityMetrics).filter(IdentityMetrics.fingerprint == fingerprint).first():
                return
                
            identity = IdentityMetrics(
                fingerprint=fingerprint,
                node_name=metrics.get('node'),
                system_os=metrics.get('system'),
                cpu_count=metrics.get('cpu_count'),
                hw_uuid=metrics.get('hw_uuid'),
                o_n_parameter=o_n
            )
            db.add(identity)
            db.commit()
        finally:
            db.close()

    def add_audit_log(self, fingerprint: str, event_type: str, description: str):
        """Añade un rastro de auditoría."""
        db = self.get_session()
        try:
            session = db.query(SystemSession).filter(SystemSession.fingerprint == fingerprint).first()
            log = AuditLog(
                session_id=session.id if session else None,
                event_type=event_type,
                description=description
            )
            db.add(log)
            db.commit()
        finally:
            db.close()
