#!/usr/bin/env python3
"""
Topology-BiMoType Mapper
========================

Maps topological states to radioactive signatures.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

import numpy as np
from typing import Dict

try:
    from ..core.datatypes import TipoDecaimiento, RADIOACTIVE_ISOTOPES
    DATATYPES_AVAILABLE = True
except ImportError:
    DATATYPES_AVAILABLE = False


class TopologyBiMoTypeMapper:
    """
    Mapea estados topológicos ternarios a firmas radiactivas BiMoType
    """
    
    # Mapeo: peso_ternario → tipo de decaimiento
    TERNARY_TO_DECAY_TYPE = {
        -1: 'BETA',      # Negativo → Beta decay (electrón)
        0:  'GAMMA',     # Neutro → Gamma decay (fotón)
        +1: 'ALPHA'      # Positivo → Alpha decay (helio)
    }
    
    # Mapeo: tipo de decaimiento → isótopo radiactivo
    DECAY_TO_ISOTOPE = {
        'BETA':  'H3',   # Tritio (Decaimiento Beta)
        'GAMMA': 'H1',   # Protio (Estable/Neutro)
        'ALPHA': 'H2'    # Deuterio (Estable/Positivo)
    }
    
    @staticmethod
    def h7_index_to_phase(h7_index: int) -> float:
        """Convierte índice H7 (0-7) a fase cuántica (0-2π)"""
        return (h7_index / 7.0) * 2.0 * np.pi
    
    @staticmethod
    def chirality_to_mg_polarity(chirality_index: float) -> float:
        """Convierte índice de quiralidad (-1 a +1) a polaridad MG (0 a 1)"""
        return (chirality_index + 1.0) / 2.0
    
    @staticmethod
    def create_radioactive_signature_from_topology(topology_state: Dict) -> Dict:
        """Crea una firma radiactiva BiMoType desde un estado topológico."""
        peso = topology_state['peso_ternario']
        decay_type = TopologyBiMoTypeMapper.TERNARY_TO_DECAY_TYPE[peso]
        isotope = TopologyBiMoTypeMapper.DECAY_TO_ISOTOPE[decay_type]
        
        phase = TopologyBiMoTypeMapper.h7_index_to_phase(
            topology_state['fase_discreta_fragmento']
        )
        
        chirality_proxy = float(topology_state['peso_ternario'])
        mg_polarity = TopologyBiMoTypeMapper.chirality_to_mg_polarity(chirality_proxy)
        
        winding = topology_state['winding']
        binding_energy_factor = 1.0 + (winding / 2.0) * 0.5
        
        if DATATYPES_AVAILABLE:
            iso_data = RADIOACTIVE_ISOTOPES[isotope]
            tipo_map = {
                'BETA': TipoDecaimiento.BETA,
                'GAMMA': TipoDecaimiento.GAMMA,
                'ALPHA': TipoDecaimiento.ALPHA
            }
            
            signature = {
                'isotope': isotope,
                'energy_peak_ev': iso_data['energy_ev'] * binding_energy_factor,
                'decay_type': tipo_map[decay_type],
                'half_life_s': iso_data['half_life_years'] * 3.154e7,
                'nuclear_spin': iso_data['spin'],
                'mahalanobis_distance': float(topology_state['indice']) / 6.0,
                'lambda_double_non_locality': float(topology_state['pareja']) / 6.0,
                'mg_polarity': mg_polarity,
                'mg_threshold': 0.5,
                'vacuum_polarity_n_r': float(topology_state['mapeo']) * 0.1,
                'quantum_phase': phase,
                'topology_encoding': topology_state
            }
        else:
            signature = {
                'isotope': isotope,
                'decay_type': decay_type,
                'quantum_phase': phase,
                'mg_polarity': mg_polarity,
                'topology_encoding': topology_state
            }
        
        return signature
