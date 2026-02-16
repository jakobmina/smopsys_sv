#!/usr/bin/env python3
"""
Ternary BiMoType Decoder
========================

Decodes BiMoType packets with noise simulation.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

import numpy as np
from typing import Dict, List

from .mapper import TopologyBiMoTypeMapper

class TernaryBiMoTypeDecoder:
    """
    Decodificador para paquetes Ternary-BiMoType
    """
    
    def __init__(self):
        self.topology_mapper = TopologyBiMoTypeMapper()
    
    def decode_bimotype_packet(
        self,
        packet: Dict,
        noise_level: float = 0.1
    ) -> Dict:
        """
        Decodifica un paquete Ternary-BiMoType.
        
        Args:
            packet: Paquete codificado
            noise_level: Nivel de ruido (0-1)
        
        Returns:
            Dict con mensaje decodificado y métricas
        """
        decoded_chars = []
        fidelities = []
        
        for qs in packet['quantum_states']:
            # 1. Simular ruido en el estado cuántico
            alpha_noisy = qs['alpha'] + np.random.normal(0, noise_level * 0.1)
            beta_noisy = qs['beta'] + np.random.normal(0, noise_level * 0.1)
            
            # Renormalizar
            norm = np.sqrt(alpha_noisy**2 + beta_noisy**2)
            alpha_noisy /= norm
            beta_noisy /= norm
            
            # 2. Reconstruir fase
            phase_reconstructed = 2.0 * np.arctan2(beta_noisy, alpha_noisy)
            
            # 3. Calcular fidelidad
            phase_original = qs['phase']
            fidelity = np.cos((phase_reconstructed - phase_original) / 2.0) ** 2
            
            # 4. Decidir si aceptar el carácter
            if fidelity > 0.7:
                decoded_chars.append(qs['character'])
                fidelities.append(fidelity)
            else:
                decoded_chars.append('?')
                fidelities.append(0.0)
        
        # Métricas
        avg_fidelity = np.mean(fidelities) if fidelities else 0.0
        
        return {
            'decoded_message': ''.join(decoded_chars),
            'original_message': packet['message'],
            'average_fidelity': avg_fidelity,
            'character_fidelities': fidelities,
            'decoding_quality': 'EXCELLENT' if avg_fidelity > 0.95 else
                               'GOOD' if avg_fidelity > 0.85 else
                               'ACCEPTABLE' if avg_fidelity > 0.70 else
                               'POOR',
            'noise_level': noise_level
        }


# ============================================================================
# GENERADOR DE CÓDIGO C PARA SMOPSYS
# ============================================================================