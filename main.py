#!/usr/bin/env python3
"""
BiMoType-Ternary: Main Entry Point
==================================

Unifica los módulos de integración de Smopsys, simulaciones metriplécticas
y criptografía cuántica.

Autor: Jacobo Tlacaelel Mina Rodriguez
"""

import sys
import argparse
import subprocess
import os
# from psimon import main as psimon_main # Removido: Usar CLI de psimon-h7 vía subprocess
from examples.demo import demo_ternary_bimotype
from examples.metriplectic_demo import run_demo as run_metriplectic_demo
from examples.generate_metriplectic_keys import MetriplecticKeyGenerator
from bimotype_ternary.network.p2p import MetriplecticPeer
from bimotype_ternary.network.discovery import PeerDiscovery

def run_crypto_demo(h7_index: int = 42):
    """Ejecuta una demostración del módulo de criptografía."""
    print("\n" + "=" * 80)
    print("  METRIPLECTIC CRYPTOGRAPHY DEMO")
    print("=" * 80)
    
    gen = MetriplecticKeyGenerator(h7_index)
    print(f"🔑 Generando secuencia de claves para H7 Index: {h7_index}...")
    keys = gen.generate_key_sequence(20)
    
    print(f"✅ Se han generado {len(keys)} claves.")
    print(f"🔒 Clave maestra [0]: {keys[0]}")
    
    # Generar visualización
    gen.plot_diagnostics()
    print("=" * 80 + "\n")

def main():
    parser = argparse.ArgumentParser(description="BiMoType-Ternary Control Center")
    
    # Subcomandos o flags
    parser.add_argument("--demo", action="store_true", help="Ejecutar demo general de integración")
    parser.add_argument("--metriplectic", action="store_true", help="Ejecutar demo de física metripléctica")
    parser.add_argument("--crypto", type=int, metavar="H7_INDEX", help="Generar claves criptográficas para un índice H7")
    parser.add_argument("--smopsys", action="store_true", help="Entrar a la CLI de Smopsys Integration (psimon)")
    
    # GUI
    parser.add_argument("--gui", action="store_true", help="Lanzar el Dashboard interactivo de Streamlit")
    
    # Networking P2P
    parser.add_argument("--listen", action="store_true", help="Escuchar paquetes BiMoType P2P")
    parser.add_argument("--send", metavar="FINGERPRINT", help="Enviar un mensaje a un fingerprint específico")
    parser.add_argument("--message", metavar="TEXT", help="Mensaje a enviar")
    parser.add_argument("--port", type=int, default=5005, help="Puerto para comunicación P2P (default: 5005)")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()
    
    if args.gui:
        print("\n[INFO] Iniciando BiMoType Dashboard...")
        # Usar el intérprete de python del venv para ejecutar streamlit como módulo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        python_executable = os.path.join(base_dir, "env", "bin", "python3")
        
        if not os.path.exists(python_executable):
            python_executable = sys.executable # Fallback al actual
            
        try:
            subprocess.run([python_executable, "-m", "streamlit", "run", "gui.py"])
        except Exception as e:
            print(f"❌ Error al iniciar el Dashboard: {e}")
        sys.exit(0)
        
    if args.demo:
        demo_ternary_bimotype()
        
    if args.metriplectic:
        run_metriplectic_demo()
        
    if args.crypto is not None:
        run_crypto_demo(args.crypto)
        
    if args.smopsys:
        print("\n[INFO] Ejecutando PSimon CLI desde la librería instalada...")
        try:
            # Ejecutar el comando 'psimon' que viene con psimon-h7
            subprocess.run(["psimon"] + sys.argv[2:])
        except FileNotFoundError:
            print("❌ Error: El comando 'psimon' no se encuentra. ¿Está instalado psimon-h7?")
        except Exception as e:
            print(f"❌ Error al ejecutar PSimon: {e}")

    if args.listen:
        peer = MetriplecticPeer(port=args.port)
        
        def on_msg(sender, packet):
            print(f"\n" + "-"*40)
            print(f"📩 PAQUETE RECIBIDO de: {sender}")
            # Decodificar usando el decoder integrado en el peer
            decoded = peer.decoder.decode_bimotype_packet(packet)
            print(f"📄 Mensaje: {decoded.get('decoded_message', 'Error al decodificar')}")
            print(f"✨ Fidelidad: {decoded.get('fidelity', 0):.4f}")
            print("-"*40 + "\n")

        peer.on_message_received = on_msg
        fp = peer.start_listening()
        
        # Registrarse localmente para que otros en la misma máquina nos encuentren
        PeerDiscovery.register_peer(fp, "127.0.0.1", args.port)
        
        print("\nPresiona Ctrl+C para dejar de escuchar...")
        while True:
            import time
            time.sleep(1)

    if args.send:
        if not args.message:
            print("❌ Error: Debes proporcionar un mensaje con --message")
            sys.exit(1)
            
        peer = MetriplecticPeer()
        target = PeerDiscovery.resolve_peer(args.send)
        
        if target:
            host, port = target
            print(f"🚀 Enviando a {args.send[:8]} en {host}:{port}...")
            peer.send_packet(host, port, args.message)
        else:
            print(f"❌ Error: No se encontró la dirección para el fingerprint {args.send}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        sys.exit(1)
