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
from psimon import main as psimon_main
from examples.demo import demo_ternary_bimotype
from examples.metriplectic_demo import run_demo as run_metriplectic_demo
from examples.generate_metriplectic_keys import MetriplecticKeyGenerator

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
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()
    
    if args.demo:
        demo_ternary_bimotype()
        
    if args.metriplectic:
        run_metriplectic_demo()
        
    if args.crypto is not None:
        run_crypto_demo(args.crypto)
        
    if args.smopsys:
        # psimon.main utiliza sys.argv, así que le pasamos lo que queda o lo llamamos directamente
        # Si queremos la ayuda de psimon, podemos simplemente delegar
        print("\n[INFO] Delegando control a PSimon CLI...")
        # Limpiamos sys.argv para que psimon no se confunda con --smopsys
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        psimon_main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        sys.exit(1)
