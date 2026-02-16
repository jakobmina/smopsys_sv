#!/usr/bin/env python3
"""
PSimon Bridge - Alias Module
=============================

Este módulo es un alias/bridge hacia psimon.py para mantener
compatibilidad con código que importa desde psimon_bridge.

Simplemente re-exporta los componentes principales de psimon.py

Autor: Jacobo Tlacaelel Mina Rodriguez
"""

# Re-exportar todo desde psimon
from psimon import (
    PSimonStub,
    IsotopeData,
    PSimonToSmopsysCodegen,
    PSIMON_AVAILABLE
)

# Alias adicionales si son necesarios
PSimonBridge = PSimonStub

__all__ = [
    'PSimonStub',
    'IsotopeData',
    'PSimonToSmopsysCodegen',
    'PSimonBridge',
    'PSIMON_AVAILABLE'
]

if __name__ == '__main__':
    print("PSimon Bridge - Re-export module")
    print(f"PSimon available: {PSIMON_AVAILABLE}")
    print(f"Isotopes in database: {len(PSimonStub.ISOTOPES)}")
