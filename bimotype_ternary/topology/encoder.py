#!/usr/bin/env python3
"""
Codificador Topológico Ternario - Big Endian
=============================================

Sistema de codificación topológica con pesos ternarios (-1, 0, +1)
compatible con el protocolo BiMoType y Smopsys Q-CORE.

Características:
- 6 estados topológicos con índices H7-compatible
- Empaquetamiento big-endian en uint16
- Codificación hexadecimal para transmisión
- Integración con quiralidad nuclear

Autor: Jacobo Tlacaelel Mina Rodriguez
"""

import numpy as np
from typing import Dict, List, Tuple, Optional


# ============================================================================
# TABLA DE ESTADOS TOPOLÓGICOS
# ============================================================================

class CodificadorTopologicoBigEndian:
    """
    Codificador topológico con empaquetamiento big-endian.
    
    Cada estado topológico tiene 6 campos:
    - indice (1-6): Índice topológico principal
    - pareja (1-6): Índice de pareja (conservación tipo H7)
    - winding (0 o 2): Número de enrollamiento
    - mapeo (0 o 1): Flag de mapeo
    - peso_ternario (-1, 0, +1): Peso ternario del estado
    - fase_discreta_fragmento (0-7): Fase discreta (compatible con H7)
    """
    
    # Tabla de 6 estados topológicos
    topology_entries = [
        {
            'indice': 1,
            'pareja': 6,
            'winding': 0,
            'mapeo': 0,
            'peso_ternario': 1,   # POSITIVO → ALPHA decay
            'fase_discreta_fragmento': 0
        },
        {
            'indice': 2,
            'pareja': 5,
            'winding': 2,
            'mapeo': 1,
            'peso_ternario': -1,  # NEGATIVO → BETA decay
            'fase_discreta_fragmento': 2
        },
        {
            'indice': 3,
            'pareja': 4,
            'winding': 0,
            'mapeo': 0,
            'peso_ternario': 0,   # NEUTRO → GAMMA decay
            'fase_discreta_fragmento': 3
        },
        {
            'indice': 4,
            'pareja': 3,
            'winding': 2,
            'mapeo': 1,
            'peso_ternario': 1,   # POSITIVO → ALPHA decay
            'fase_discreta_fragmento': 5
        },
        {
            'indice': 5,
            'pareja': 2,
            'winding': 0,
            'mapeo': 0,
            'peso_ternario': -1,  # NEGATIVO → BETA decay
            'fase_discreta_fragmento': 6
        },
        {
            'indice': 6,
            'pareja': 1,
            'winding': 2,
            'mapeo': 1,
            'peso_ternario': 0,   # NEUTRO → GAMMA decay
            'fase_discreta_fragmento': 7
        }
    ]
    
    @staticmethod
    def empaquetar_topologia(
        indice: int,
        pareja: int,
        winding: int,
        mapeo: int,
        peso_ternario: int,
        fase_discreta_fragmento: int
    ) -> int:
        """
        Empaqueta los 6 campos en un uint16 (big-endian).
        
        Layout de bits (16 bits total):
        - Bits 15-13 (3 bits): indice (1-6, necesita 3 bits)
        - Bits 12-10 (3 bits): pareja (1-6, necesita 3 bits)
        - Bits 9-8   (2 bits): winding (0 o 2, codificado como 0 o 1)
        - Bit  7     (1 bit):  mapeo (0 o 1)
        - Bits 6-5   (2 bits): peso_ternario (-1, 0, +1, codificado como 0, 1, 2)
        - Bits 4-0   (5 bits): fase_discreta_fragmento (0-7, necesita 3 bits, pero dejamos 5 para expansión)
        
        Args:
            indice: 1-6
            pareja: 1-6
            winding: 0 o 2
            mapeo: 0 o 1
            peso_ternario: -1, 0, +1
            fase_discreta_fragmento: 0-7
        
        Returns:
            uint16 empaquetado
        """
        # Validaciones
        assert 1 <= indice <= 6, f"indice debe estar en [1, 6]: {indice}"
        assert 1 <= pareja <= 6, f"pareja debe estar en [1, 6]: {pareja}"
        assert winding in [0, 2], f"winding debe ser 0 o 2: {winding}"
        assert mapeo in [0, 1], f"mapeo debe ser 0 o 1: {mapeo}"
        assert peso_ternario in [-1, 0, 1], f"peso_ternario debe ser -1, 0, o 1: {peso_ternario}"
        assert 0 <= fase_discreta_fragmento <= 7, f"fase debe estar en [0, 7]: {fase_discreta_fragmento}"
        
        # Codificar winding: 0 → 0, 2 → 1
        winding_encoded = winding // 2
        
        # Codificar peso_ternario: -1 → 0, 0 → 1, +1 → 2
        peso_encoded = peso_ternario + 1
        
        # Empaquetar (big-endian)
        packed = 0
        packed |= (indice & 0x7) << 13           # Bits 15-13
        packed |= (pareja & 0x7) << 10           # Bits 12-10
        packed |= (winding_encoded & 0x3) << 8   # Bits 9-8
        packed |= (mapeo & 0x1) << 7             # Bit 7
        packed |= (peso_encoded & 0x3) << 5      # Bits 6-5
        packed |= (fase_discreta_fragmento & 0x1F)  # Bits 4-0
        
        return packed
    
    @staticmethod
    def desempaquetar_topologia(packed: int) -> Dict:
        """
        Desempaqueta un uint16 en los 6 campos topológicos.
        
        Args:
            packed: uint16 empaquetado
        
        Returns:
            Dict con los 6 campos
        """
        # Extraer campos
        indice = (packed >> 13) & 0x7
        pareja = (packed >> 10) & 0x7
        winding_encoded = (packed >> 8) & 0x3
        mapeo = (packed >> 7) & 0x1
        peso_encoded = (packed >> 5) & 0x3
        fase_discreta_fragmento = packed & 0x1F
        
        # Decodificar winding: 0 → 0, 1 → 2
        winding = winding_encoded * 2
        
        # Decodificar peso_ternario: 0 → -1, 1 → 0, 2 → +1
        peso_ternario = peso_encoded - 1
        
        return {
            'indice': indice,
            'pareja': pareja,
            'winding': winding,
            'mapeo': mapeo,
            'peso_ternario': peso_ternario,
            'fase_discreta_fragmento': fase_discreta_fragmento
        }
    
    @classmethod
    def obtener_estado_topologico(cls, index: int) -> Dict:
        """
        Obtiene un estado topológico por índice (0-5).
        
        Args:
            index: 0-5
        
        Returns:
            Dict con estado topológico
        """
        if not 0 <= index < len(cls.topology_entries):
            raise ValueError(f"Índice fuera de rango: {index}")
        
        return cls.topology_entries[index].copy()


# ============================================================================
# CODIFICADOR HEXADECIMAL
# ============================================================================

class CodificadorHexadecimalBigEndian:
    """
    Codificador hexadecimal para valores empaquetados.
    """
    
    @staticmethod
    def a_hex_uint16(value: int) -> str:
        """
        Convierte uint16 a string hexadecimal (4 dígitos).
        
        Args:
            value: uint16 (0-65535)
        
        Returns:
            String hexadecimal "XXXX"
        """
        return f"{value:04X}"
    
    @staticmethod
    def desde_hex_uint16(hex_str: str) -> int:
        """
        Convierte string hexadecimal a uint16.
        
        Args:
            hex_str: String hexadecimal "XXXX"
        
        Returns:
            uint16
        """
        return int(hex_str, 16)
    
    @staticmethod
    def a_binario_uint16(value: int) -> str:
        """
        Convierte uint16 a string binario (16 bits).
        
        Args:
            value: uint16
        
        Returns:
            String binario "XXXXXXXXXXXXXXXX"
        """
        return f"{value:016b}"


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def generar_tabla_topologica_completa() -> List[Dict]:
    """
    Genera tabla completa con valores empaquetados y hex.
    
    Returns:
        Lista de dicts con todos los campos
    """
    tabla = []
    
    for entry in CodificadorTopologicoBigEndian.topology_entries:
        # Empaquetar
        packed = CodificadorTopologicoBigEndian.empaquetar_topologia(
            entry['indice'],
            entry['pareja'],
            entry['winding'],
            entry['mapeo'],
            entry['peso_ternario'],
            entry['fase_discreta_fragmento']
        )
        
        # Hex
        hex_val = CodificadorHexadecimalBigEndian.a_hex_uint16(packed)
        
        # Binario
        bin_val = CodificadorHexadecimalBigEndian.a_binario_uint16(packed)
        
        # Compilar
        entry_completo = entry.copy()
        entry_completo['packed_uint16'] = packed
        entry_completo['hex_encoding'] = hex_val
        entry_completo['binary_encoding'] = bin_val
        
        tabla.append(entry_completo)
    
    return tabla


# ============================================================================
# DEMO
# ============================================================================

def demo_codificador_topologico():
    """Demuestra el codificador topológico"""
    
    print("=" * 80)
    print("  CODIFICADOR TOPOLÓGICO TERNARIO - BIG ENDIAN")
    print("=" * 80)
    
    # Generar tabla completa
    tabla = generar_tabla_topologica_completa()
    
    print("\nTABLA DE ESTADOS TOPOLÓGICOS:")
    print("-" * 80)
    print(f"{'Idx':<4} {'Indice':<7} {'Pareja':<7} {'Wind':<5} {'Map':<4} {'Peso':<5} {'Fase':<5} {'Hex':<6} {'Packed':<7}")
    print("-" * 80)
    
    for i, entry in enumerate(tabla):
        print(
            f"{i:<4} "
            f"{entry['indice']:<7} "
            f"{entry['pareja']:<7} "
            f"{entry['winding']:<5} "
            f"{entry['mapeo']:<4} "
            f"{entry['peso_ternario']:+2d}   "
            f"{entry['fase_discreta_fragmento']:<5} "
            f"{entry['hex_encoding']:<6} "
            f"{entry['packed_uint16']:<7}"
        )
    
    # Test de empaquetamiento/desempaquetamiento
    print("\n\nTEST DE EMPAQUETAMIENTO/DESEMPAQUETAMIENTO:")
    print("-" * 80)
    
    for i, entry in enumerate(tabla):
        # Desempaquetar
        unpacked = CodificadorTopologicoBigEndian.desempaquetar_topologia(
            entry['packed_uint16']
        )
        
        # Verificar
        match = all([
            unpacked['indice'] == entry['indice'],
            unpacked['pareja'] == entry['pareja'],
            unpacked['winding'] == entry['winding'],
            unpacked['mapeo'] == entry['mapeo'],
            unpacked['peso_ternario'] == entry['peso_ternario'],
            unpacked['fase_discreta_fragmento'] == entry['fase_discreta_fragmento']
        ])
        
        status = "✓" if match else "✗"
        print(f"{status} Estado {i}: {entry['hex_encoding']} → {unpacked}")
    
    # Mapeo a tipos de decaimiento
    print("\n\nMAPEO PESO TERNARIO → TIPO DE DECAIMIENTO:")
    print("-" * 80)
    
    decay_map = {
        -1: 'BETA  (β⁻)',
        0:  'GAMMA (γ)',
        1:  'ALPHA (α)'
    }
    
    for entry in tabla:
        peso = entry['peso_ternario']
        decay = decay_map[peso]
        print(f"Estado {entry['indice']}: peso={peso:+2d} → {decay}")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETO")
    print("=" * 80)


if __name__ == '__main__':
    demo_codificador_topologico()
