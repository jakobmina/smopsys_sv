"""
BiMoType-Ternary Integration Framework
======================================

Quantum communication protocol with radioactive signatures and topological encoding.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

__version__ = "1.0.0"
__author__ = "Jacobo Tlacaelel Mina Rodriguez"

# Core components
from .core.datatypes import (
    FirmaRadiactiva,
    EstadoCuantico,
    TipoDecaimiento,
    PaqueteBiMoType,
    RADIOACTIVE_ISOTOPES
)

# Topology encoder
from .topology.encoder import (
    CodificadorTopologicoBigEndian,
    CodificadorHexadecimalBigEndian
)

# Integration
from .integration.mapper import TopologyBiMoTypeMapper
from .integration.encoder import TernaryBiMoTypeEncoder
from .integration.decoder import TernaryBiMoTypeDecoder

# Code generation
from .codegen.c_generator import TernaryBiMoTypeCodegen

__all__ = [
    # Core
    'FirmaRadiactiva',
    'EstadoCuantico',
    'TipoDecaimiento',
    'PaqueteBiMoType',
    'RADIOACTIVE_ISOTOPES',
    
    # Topology
    'CodificadorTopologicoBigEndian',
    'CodificadorHexadecimalBigEndian',
    
    # Integration
    'TopologyBiMoTypeMapper',
    'TernaryBiMoTypeEncoder',
    'TernaryBiMoTypeDecoder',
    
    # Codegen
    'TernaryBiMoTypeCodegen',
]
