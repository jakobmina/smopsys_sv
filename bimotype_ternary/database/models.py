from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class SystemSession(Base):
    """
    Componente Simpléctica: Representa la integridad estructural de una sesión.
    Guarda el estado base de ejecución.
    """
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    session_number = Column(Integer, nullable=False)
    fingerprint = Column(String, unique=True, nullable=False)
    startup_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='ACTIVE')
    
    # Relación con el estado recursivo (la memoria del sistema)
    state = relationship("RecursiveState", back_populates="session", uselist=False)
    # Relación con eventos de auditoría
    audit_events = relationship("AuditLog", back_populates="session")

class RecursiveState(Base):
    """
    Componente Métrica: Representa la memoria evolutiva del sistema.
    Almacena el payload de información que se propaga entre ciclos.
    """
    __tablename__ = 'recursive_states'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), unique=True)
    payload = Column(JSON, nullable=False) # El "genoma" informacional
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    session = relationship("SystemSession", back_populates="state")

class IdentityMetrics(Base):
    """
    Fondo Estructurado (O_n): Metadata del hardware detectado.
    """
    __tablename__ = 'identity_metrics'
    
    id = Column(Integer, primary_key=True)
    fingerprint = Column(String, unique=True, nullable=False)
    node_name = Column(String)
    system_os = Column(String)
    cpu_count = Column(Integer)
    hw_uuid = Column(String)
    o_n_parameter = Column(Float) # Modulación del Operador Áureo
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    """
    Componente de Disipación: Registro de eventos irreversibles.
    """
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    event_type = Column(String, nullable=False)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("SystemSession", back_populates="audit_events")
