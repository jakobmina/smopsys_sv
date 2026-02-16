#!/usr/bin/env python3
"""
Ternary BiMoType Encoder
========================

Encodes messages using topology + BiMoType.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

import numpy as np
import time
from typing import Dict, List
from collections import Counter

try:
    from ..topology.encoder import CodificadorTopologicoBigEndian, CodificadorHexadecimalBigEndian
    TOPOLOGY_AVAILABLE = True
except ImportError:
    TOPOLOGY_AVAILABLE = False

try:
    from ..utils.psimon_bridge import PSimonStub
    PSIMON_AVAILABLE = True
except ImportError:
    PSIMON_AVAILABLE = False

from .mapper import TopologyBiMoTypeMapper

class TernaryBiMoTypeEncoder:
    """
    Codificador que combina topología ternaria con BiMoType
    """
    
    def __init__(self):
        self.topology_mapper = TopologyBiMoTypeMapper()
        
        # Tabla de estados topológicos (de mod6_mejorado.py)
        if TOPOLOGY_AVAILABLE:
            self.topology_entries = CodificadorTopologicoBigEndian.topology_entries
        else:
            # Stub básico
            self.topology_entries = [
                {
                    'indice': 1, 'pareja': 6, 'winding': 0, 'mapeo': 0,
                    'peso_ternario': 1, 'fase_discreta_fragmento': 0
                }
            ]
    
    def encode_message_with_topology(
        self,
        message: str,
        use_nuclear_isotopes: bool = True
    ) -> Dict:
        """
        Codifica un mensaje usando topología ternaria + BiMoType.
        
        Para cada carácter:
        1. Selecciona un estado topológico
        2. Crea firma radiactiva correspondiente
        3. Genera estado cuántico BiMoType
        
        Args:
            message: Mensaje a codificar
            use_nuclear_isotopes: Si True, usa isótopos de PSimon también
        
        Returns:
            Dict con encoding completo
        """
        encoded_chars = []
        
        for i, char in enumerate(message.upper()):
            # 1. Seleccionar estado topológico (rotar por la tabla)
            topo_idx = i % len(self.topology_entries)
            topology_state = self.topology_entries[topo_idx].copy()
            
            # 2. Si tenemos PSimon, enriquecer con datos nucleares
            if use_nuclear_isotopes and PSIMON_AVAILABLE:
                # Mapear char a isótopo (simplificado)
                isotope_map = {
                    'H': 'H', 'D': 'D', 'T': 'T',
                    'A': 'He-3', 'B': 'He-4'
                }
                isotope_name = isotope_map.get(char, 'H')
                nuclear_data = PSimonStub.get_isotope(isotope_name)
                
                if nuclear_data:
                    # Enriquecer estado topológico con datos nucleares
                    topology_state['nuclear_isotope'] = nuclear_data.name
                    topology_state['h7_index'] = nuclear_data.h7_index
                    topology_state['nuclear_chirality'] = nuclear_data.chirality_index
                    
                    # Actualizar fase discreta desde H7
                    topology_state['fase_discreta_fragmento'] = nuclear_data.h7_index
            
            # 3. Crear firma radiactiva
            radioactive_signature = self.topology_mapper.create_radioactive_signature_from_topology(
                topology_state
            )
            
            # 4. Empaquetar en formato hexadecimal
            if TOPOLOGY_AVAILABLE:
                packed_value = CodificadorTopologicoBigEndian.empaquetar_topologia(
                    topology_state['indice'],
                    topology_state['pareja'],
                    topology_state['winding'],
                    topology_state['mapeo'],
                    topology_state['peso_ternario'],
                    topology_state['fase_discreta_fragmento']
                )
                hex_encoding = CodificadorHexadecimalBigEndian.a_hex_uint16(packed_value)
            else:
                packed_value = 0
                hex_encoding = "0000"
            
            # 5. Compilar datos del carácter
            char_encoding = {
                'character': char,
                'position': i,
                'topology_state': topology_state,
                'radioactive_signature': radioactive_signature,
                'hex_encoding': hex_encoding,
                'packed_value': packed_value
            }
            
            encoded_chars.append(char_encoding)
        
        return {
            'message': message,
            'encoded_characters': encoded_chars,
            'encoding_method': 'Ternary-BiMoType-Hybrid',
            'timestamp': time.time()
        }
    
    def create_bimotype_packet_from_ternary(
        self,
        encoded_message: Dict
    ) -> Dict:
        """
        Crea un paquete BiMoType completo desde mensaje codificado ternario.
        """
        # Estados cuánticos para cada carácter
        quantum_states = []
        
        for char_enc in encoded_message['encoded_characters']:
            sig = char_enc['radioactive_signature']
            phase = sig['quantum_phase']
            
            # Estado cuántico: |ψ⟩ = cos(φ/2)|0⟩ + sin(φ/2)|1⟩
            alpha = np.cos(phase / 2.0)
            beta = np.sin(phase / 2.0)
            
            quantum_state = {
                'character': char_enc['character'],
                'alpha': float(alpha),
                'beta': float(beta),
                'phase': float(phase),
                'isotope': sig['isotope'],
                'energy': sig.get('energy_peak_ev', 0.0),
                'decay_type': str(sig['decay_type']),
                'topology_hex': char_enc['hex_encoding']
            }
            
            quantum_states.append(quantum_state)
        
        # Paquete completo
        packet = {
            'packet_id': f"TERNARY-BIMO-{int(time.time())}-{abs(hash(encoded_message['message'])) % 10000:04d}",
            'protocol': 'Ternary-BiMoType-v1.0',
            'timestamp': time.time(),
            'message': encoded_message['message'],
            'quantum_states': quantum_states,
            'encoding_metadata': {
                'total_characters': len(quantum_states),
                'total_energy_ev': sum(qs['energy'] for qs in quantum_states),
                'average_phase': np.mean([qs['phase'] for qs in quantum_states]),
                'decay_types_distribution': self._count_decay_types(quantum_states)
            }
        }
        
        return packet
    
    @staticmethod
    def _count_decay_types(quantum_states: List[Dict]) -> Dict:
        """Cuenta distribución de tipos de decaimiento"""
        from collections import Counter
        decay_types = [qs['decay_type'] for qs in quantum_states]
        return dict(Counter(decay_types))


# ============================================================================
# DECODIFICADOR TERNARY-BIMOTYPE
# ============================================================================