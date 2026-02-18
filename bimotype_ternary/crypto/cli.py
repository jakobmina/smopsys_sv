#!/usr/bin/env python3
"""
Quantum Crypto CLI
==================

Command-line interface for quantum password generation and encryption.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

import click
import sys
import json
from .password_generator import QuantumPasswordGenerator
from .encryptor import QuantumEncryptor
from ..core.session_manager import SessionManager
from ..database.manager import DatabaseManager
from ..database.models import SystemSession, IdentityMetrics, AuditLog

# Global Session Manager for the CLI lifecycle
_session_manager = None

def get_sm():
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    BiMoType Quantum Cryptography CLI (Metriplectic Agent)
    
    Genera contraseñas seguras y encripta datos con transparencia absoluta.
    """
    # Iniciar sesión automáticamente en cada ejecución del comando
    get_sm().start_session()

@cli.command()
@click.option('--length', '-l', default=16, help='Longitud de la contraseña')
@click.option('--charset', '-c', default='alphanumeric+symbols', help='Juego de caracteres')
@click.option('--count', '-n', default=1, help='Número de contraseñas')
def password(length, charset, count):
    """Genera contraseñas cuánticas seguras."""
    sm = get_sm()
    try:
        gen = QuantumPasswordGenerator()
        for i in range(count):
            pwd = gen.generate(length=length, charset=charset)
            click.echo(pwd)
            sm.engine.db.add_audit_log(sm.current_fingerprint, "PWD_GEN", f"Contraseña de {length} caracteres generada.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--input', '-i', 'input_file', required=True, help='Archivo a encriptar')
@click.option('--output', '-o', 'output_file', required=True, help='Archivo de salida')
@click.password_option(help='Contraseña de cifrado')
def encrypt(input_file, output_file, password):
    """Encripta un archivo usando llaves derivadas cuánticamente."""
    sm = get_sm()
    try:
        encryptor = QuantumEncryptor()
        encryptor.encrypt_file(input_file, output_file, password)
        sm.engine.db.add_audit_log(sm.current_fingerprint, "FILE_ENC", f"Archivo {input_file} encriptado.")
        click.echo(f"✓ Encriptado correctamente en {output_file}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--input', '-i', 'input_file', required=True, help='Archivo encriptado')
@click.option('--output', '-o', 'output_file', required=True, help='Archivo de salida')
@click.password_option(help='Contraseña de descifrado')
def decrypt(input_file, output_file, password):
    """Descifra un archivo."""
    sm = get_sm()
    try:
        encryptor = QuantumEncryptor()
        encryptor.decrypt_file(input_file, output_file, password)
        sm.engine.db.add_audit_log(sm.current_fingerprint, "FILE_DEC", f"Archivo {input_file} descifrado.")
        click.echo(f"✓ Descifrado correctamente en {output_file}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.group()
def audit():
    """Herramientas de transparencia y auditoría Metripléctica."""
    pass

@audit.command(name='sessions')
@click.option('--limit', '-n', default=10, help='Número de sesiones a mostrar')
def audit_sessions(limit):
    """Lista los últimos ciclos de ejecución del sistema."""
    sm = get_sm()
    db = sm.engine.db.get_session()
    try:
        sessions = db.query(SystemSession).order_by(SystemSession.id.desc()).limit(limit).all()
        click.echo(f"\n{'ID':<5} {'N':<3} {'Fingerprint':<20} {'Startup Time':<20}")
        click.echo("-" * 60)
        for s in sessions:
            click.echo(f"{s.id:<5} {s.session_number:<3} {s.fingerprint[:18]}... {s.startup_time}")
    finally:
        db.close()

@audit.command(name='logs')
@click.option('--limit', '-n', default=15, help='Número de eventos a mostrar')
def audit_logs(limit):
    """Muestra el historial de eventos del sistema."""
    sm = get_sm()
    db = sm.engine.db.get_session()
    try:
        logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(limit).all()
        click.echo(f"\n{'Timestamp':<20} {'Event':<12} {'Description'}")
        click.echo("-" * 70)
        for l in logs:
            click.echo(f"{l.timestamp.strftime('%Y-%m-%d %H:%M:%S'):<20} {l.event_type:<12} {l.description}")
    finally:
        db.close()

@audit.command(name='identity')
def audit_identity():
    """Muestra la identidad de hardware actual."""
    sm = get_sm()
    db = sm.engine.db.get_session()
    try:
        metrics = db.query(IdentityMetrics).filter(IdentityMetrics.fingerprint == sm.current_fingerprint).first()
        if metrics:
            click.echo(f"\nIdentidad Metripléctica Detectada:")
            click.echo(f"  Node:       {metrics.node_name}")
            click.echo(f"  OS:         {metrics.system_os}")
            click.echo(f"  CPU Count:  {metrics.cpu_count}")
            click.echo(f"  HW UUID:    {metrics.hw_uuid}")
            click.echo(f"  O_n Param:  {metrics.o_n_parameter:.6f}")
            click.echo(f"  Fingerprint: {metrics.fingerprint}")
        else:
            click.echo("No se encontró información de identidad en esta sesión.")
    finally:
        db.close()

if __name__ == '__main__':
    cli()
