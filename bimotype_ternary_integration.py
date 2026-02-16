#!/usr/bin/env python3
"""
BiMoType + Ternary Topology Integration
========================================

Integra el protocolo BiMoType con el sistema de codificación topológica ternaria.

Combina:
1. BiMoType Protocol → Comunicación cuántica radiactiva
2. Topology Encoder → Estados ternarios (-1, 0, +1)
3. PSimon Nuclear → Isótopos y H7 conservation
4. QuoreMind Bayesian → Lógica de decisión

Mapeo conceptual:
- Peso ternario (-1, 0, +1) → Tipo de decaimiento radiactivo
- Índice H7 → Fase de enrollamiento topológico
- Quiralidad → Polaridad MG (Mahalanobis-Gravedad)
- Estados cuánticos → Firmas radiactivas

Autor: Jacobo Tlacaelel Mina Rodriguez
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import time

# Importar componentes base
try:
    from mod6_mejorado import (
        CodificadorTopologicoBigEndian,
        CodificadorHexadecimalBigEndian
    )
    TOPOLOGY_AVAILABLE = True
except ImportError:
    TOPOLOGY_AVAILABLE = False
    print("[WARNING] Topology encoder not available")

try:
    from psimon_bridge import PSimonStub, IsotopeData
    PSIMON_AVAILABLE = True
except ImportError:
    PSIMON_AVAILABLE = False
    print("[WARNING] PSimon not available")

try:
    from datatypes import FirmaRadiactiva, TipoDecaimiento, RADIOACTIVE_ISOTOPES
    DATATYPES_AVAILABLE = True
except ImportError:
    DATATYPES_AVAILABLE = False
    print("[WARNING] BiMoType datatypes not available")


# ============================================================================
# MAPEO TOPOLÓGICO ↔ BIMOTYPE
# ============================================================================

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
        'BETA':  'Sr90',   # Beta minus
        'GAMMA': 'Tc99m',  # Gamma puro
        'ALPHA': 'Pu238'   # Alpha
    }
    
    # Mapeo: índice H7 → fase cuántica (0-7 → 0-2π)
    @staticmethod
    def h7_index_to_phase(h7_index: int) -> float:
        """
        Convierte índice H7 (0-7) a fase cuántica (0-2π)
        """
        return (h7_index / 7.0) * 2.0 * np.pi
    
    # Mapeo: quiralidad → polaridad MG
    @staticmethod
    def chirality_to_mg_polarity(chirality_index: float) -> float:
        """
        Convierte índice de quiralidad (-1 a +1) a polaridad MG (0 a 1)
        """
        return (chirality_index + 1.0) / 2.0
    
    @staticmethod
    def create_radioactive_signature_from_topology(
        topology_state: Dict
    ) -> Dict:
        """
        Crea una firma radiactiva BiMoType desde un estado topológico.
        
        Args:
            topology_state: Dict con keys:
                - indice: 1-6
                - pareja: 1-6
                - winding: 0 o 2
                - mapeo: 0 o 1
                - peso_ternario: -1, 0, +1
                - fase_discreta_fragmento: 0-7
        
        Returns:
            Dict compatible con FirmaRadiactiva de BiMoType
        """
        # 1. Determinar tipo de decaimiento desde peso ternario
        peso = topology_state['peso_ternario']
        decay_type = TopologyBiMoTypeMapper.TERNARY_TO_DECAY_TYPE[peso]
        isotope = TopologyBiMoTypeMapper.DECAY_TO_ISOTOPE[decay_type]
        
        # 2. Calcular fase cuántica desde fase_discreta_fragmento
        phase = TopologyBiMoTypeMapper.h7_index_to_phase(
            topology_state['fase_discreta_fragmento']
        )
        
        # 3. Mapear quiralidad (si está disponible)
        # Asumimos que quiralidad viene de otro lugar, usamos peso como proxy
        chirality_proxy = float(topology_state['peso_ternario'])
        mg_polarity = TopologyBiMoTypeMapper.chirality_to_mg_polarity(chirality_proxy)
        
        # 4. Calcular parámetros radiactivos
        # Winding → energía de enlace
        winding = topology_state['winding']
        binding_energy_factor = 1.0 + (winding / 2.0) * 0.5  # 0 o 2 → 1.0 o 2.0
        
        # 5. Construir firma
        if DATATYPES_AVAILABLE:
            # Datos base del isótopo
            iso_data = RADIOACTIVE_ISOTOPES[isotope]
            
            # Mapear tipo de decaimiento a TipoDecaimiento enum
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
            # Fallback sin datatypes
            signature = {
                'isotope': isotope,
                'decay_type': decay_type,
                'quantum_phase': phase,
                'mg_polarity': mg_polarity,
                'topology_encoding': topology_state
            }
        
        return signature


# ============================================================================
# CODIFICADOR HÍBRIDO TOPOLOGÍA + BIMOTYPE
# ============================================================================

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

class TernaryBiMoTypeCodegen:
    """Genera código C para Smopsys"""
    
    @staticmethod
    def generate_header() -> str:
        """Genera ternary_bimotype.h"""
        
        code = """/*
 * ternary_bimotype.h - Integración Ternary + BiMoType
 * Smopsys Q-CORE
 * 
 * AUTO-GENERATED from bimotype_ternary_integration.py
 */

#ifndef TERNARY_BIMOTYPE_H
#define TERNARY_BIMOTYPE_H

#include <stdint.h>
#include <math.h>

/* ============================================================
 * TIPOS DE DECAIMIENTO RADIACTIVO
 * ============================================================ */

typedef enum {
    DECAY_BETA,   // peso_ternario = -1
    DECAY_GAMMA,  // peso_ternario = 0
    DECAY_ALPHA   // peso_ternario = +1
} DecayType;

/* ============================================================
 * ESTADO TOPOLÓGICO
 * ============================================================ */

typedef struct {
    uint8_t indice;
    uint8_t pareja;
    uint8_t winding;
    uint8_t mapeo;
    int8_t peso_ternario;
    uint8_t fase_discreta_fragmento;
} TopologicalState;

/* ============================================================
 * FIRMA RADIACTIVA TOPOLÓGICA
 * ============================================================ */

typedef struct {
    // Datos topológicos
    TopologicalState topology;
    
    // Datos radiactivos
    const char *isotope;
    DecayType decay_type;
    float energy_peak_ev;
    float half_life_s;
    float nuclear_spin;
    
    // Métricas cuánticas
    float mahalanobis_distance;
    float lambda_double_non_locality;
    float mg_polarity;
    float quantum_phase;
    
    // Empaquetamiento
    uint16_t packed_topology;
    char hex_encoding[5];  // "XXXX\0"
} TernaryRadioactiveSignature;

/* ============================================================
 * MAPEO TERNARIO → DECAIMIENTO
 * ============================================================ */

static inline DecayType ternary_to_decay_type(int8_t peso_ternario) {
    switch (peso_ternario) {
        case -1: return DECAY_BETA;
        case  0: return DECAY_GAMMA;
        case  1: return DECAY_ALPHA;
        default: return DECAY_GAMMA;
    }
}

static inline const char* decay_type_to_isotope(DecayType type) {
    switch (type) {
        case DECAY_BETA:  return "Sr90";
        case DECAY_GAMMA: return "Tc99m";
        case DECAY_ALPHA: return "Pu238";
        default: return "Tc99m";
    }
}

/* ============================================================
 * CONVERSIÓN H7 → FASE CUÁNTICA
 * ============================================================ */

static inline float h7_index_to_phase(uint8_t h7_index) {
    // 0-7 → 0-2π
    return ((float)h7_index / 7.0f) * 2.0f * 3.14159265f;
}

static inline float chirality_to_mg_polarity(float chirality_index) {
    // -1 a +1 → 0 a 1
    return (chirality_index + 1.0f) / 2.0f;
}

/* ============================================================
 * EMPAQUETAMIENTO TOPOLÓGICO
 * ============================================================ */

static inline uint16_t topology_pack(const TopologicalState *topo) {
    uint16_t packed = 0;
    
    // Codificar winding: 0 → 0, 2 → 1
    uint8_t winding_encoded = topo->winding / 2;
    
    // Codificar peso_ternario: -1 → 0, 0 → 1, +1 → 2
    uint8_t peso_encoded = topo->peso_ternario + 1;
    
    // Empaquetar (big-endian)
    packed |= (topo->indice & 0x7) << 13;
    packed |= (topo->pareja & 0x7) << 10;
    packed |= (winding_encoded & 0x3) << 8;
    packed |= (topo->mapeo & 0x1) << 7;
    packed |= (peso_encoded & 0x3) << 5;
    packed |= (topo->fase_discreta_fragmento & 0x1F);
    
    return packed;
}

static inline void topology_to_hex16(uint16_t packed, char *hex_out) {
    // Convertir a hex string "XXXX"
    const char hex_chars[] = "0123456789ABCDEF";
    hex_out[0] = hex_chars[(packed >> 12) & 0xF];
    hex_out[1] = hex_chars[(packed >> 8) & 0xF];
    hex_out[2] = hex_chars[(packed >> 4) & 0xF];
    hex_out[3] = hex_chars[packed & 0xF];
    hex_out[4] = '\\0';
}

/* ============================================================
 * CREAR FIRMA DESDE TOPOLOGÍA
 * ============================================================ */

static inline void create_radioactive_signature_from_topology(
    const TopologicalState *topo,
    TernaryRadioactiveSignature *sig
) {
    // Copiar datos topológicos
    sig->topology = *topo;
    
    // Determinar tipo de decaimiento
    sig->decay_type = ternary_to_decay_type(topo->peso_ternario);
    sig->isotope = decay_type_to_isotope(sig->decay_type);
    
    // Calcular fase cuántica
    sig->quantum_phase = h7_index_to_phase(topo->fase_discreta_fragmento);
    
    // Energía según tipo de decaimiento + winding
    float binding_factor = 1.0f + ((float)topo->winding / 2.0f) * 0.5f;
    
    switch (sig->decay_type) {
        case DECAY_BETA:
            sig->energy_peak_ev = 0.546f * binding_factor;
            sig->half_life_s = 28.8f * 3.154e7f;
            sig->nuclear_spin = 0.0f;
            break;
        case DECAY_GAMMA:
            sig->energy_peak_ev = 0.14f * binding_factor;
            sig->half_life_s = 0.25f * 3.154e7f;
            sig->nuclear_spin = 4.5f;
            break;
        case DECAY_ALPHA:
            sig->energy_peak_ev = 5.59f * binding_factor;
            sig->half_life_s = 87.7f * 3.154e7f;
            sig->nuclear_spin = 0.0f;
            break;
    }
    
    // Métricas cuánticas
    sig->mahalanobis_distance = (float)topo->indice / 6.0f;
    sig->lambda_double_non_locality = (float)topo->pareja / 6.0f;
    sig->mg_polarity = chirality_to_mg_polarity((float)topo->peso_ternario);
    
    // Empaquetar
    sig->packed_topology = topology_pack(topo);
    topology_to_hex16(sig->packed_topology, sig->hex_encoding);
}

/* ============================================================
 * ESTADO CUÁNTICO DESDE FIRMA
 * ============================================================ */

typedef struct {
    float alpha;  // cos(φ/2)
    float beta;   // sin(φ/2)
    float phase;
    const char *isotope;
    float energy;
} TernaryQuantumState;

static inline void create_quantum_state_from_signature(
    const TernaryRadioactiveSignature *sig,
    TernaryQuantumState *state
) {
    float phase = sig->quantum_phase;
    
    state->alpha = cosf(phase / 2.0f);
    state->beta = sinf(phase / 2.0f);
    state->phase = phase;
    state->isotope = sig->isotope;
    state->energy = sig->energy_peak_ev;
}

#endif /* TERNARY_BIMOTYPE_H */
"""
        
        return code


# ============================================================================
# DEMO
# ============================================================================

def demo_ternary_bimotype():
    """Demuestra integración completa"""
    
    print("=" * 80)
    print("  TERNARY-BIMOTYPE INTEGRATION DEMO")
    print("=" * 80)
    
    # 1. Crear encoder
    encoder = TernaryBiMoTypeEncoder()
    
    # 2. Codificar mensaje
    message = "HELLO"
    print(f"\n1. ENCODING MESSAGE: '{message}'")
    print("-" * 80)
    
    encoded = encoder.encode_message_with_topology(
        message,
        use_nuclear_isotopes=PSIMON_AVAILABLE
    )
    
    print(f"Characters encoded: {len(encoded['encoded_characters'])}")
    
    for char_enc in encoded['encoded_characters'][:3]:  # Mostrar primeros 3
        print(f"\nCharacter: {char_enc['character']}")
        print(f"  Topology hex: {char_enc['hex_encoding']}")
        sig = char_enc['radioactive_signature']
        print(f"  Isotope: {sig['isotope']}")
        print(f"  Decay type: {sig['decay_type']}")
        print(f"  Energy: {sig.get('energy_peak_ev', 0.0):.3f} eV")
        print(f"  Phase: {sig['quantum_phase']:.4f} rad")
        print(f"  MG polarity: {sig['mg_polarity']:.3f}")
    
    # 3. Crear paquete BiMoType
    print(f"\n2. CREATING BIMOTYPE PACKET")
    print("-" * 80)
    
    packet = encoder.create_bimotype_packet_from_ternary(encoded)
    
    print(f"Packet ID: {packet['packet_id']}")
    print(f"Total energy: {packet['encoding_metadata']['total_energy_ev']:.3f} eV")
    print(f"Average phase: {packet['encoding_metadata']['average_phase']:.4f} rad")
    print(f"Decay types: {packet['encoding_metadata']['decay_types_distribution']}")
    
    # 4. Decodificar
    print(f"\n3. DECODING PACKET (noise=0.1)")
    print("-" * 80)
    
    decoder = TernaryBiMoTypeDecoder()
    decoded = decoder.decode_bimotype_packet(packet, noise_level=0.1)
    
    print(f"Original:  {decoded['original_message']}")
    print(f"Decoded:   {decoded['decoded_message']}")
    print(f"Fidelity:  {decoded['average_fidelity']:.4f}")
    print(f"Quality:   {decoded['decoding_quality']}")
    
    # 5. Generar código C
    print(f"\n4. GENERATING C CODE")
    print("-" * 80)
    
    codegen = TernaryBiMoTypeCodegen()
    header = codegen.generate_header()
    
    with open('ternary_bimotype.h', 'w') as f:
        f.write(header)
    
    print("✓ Generated: ternary_bimotype.h")
    
    # 6. Guardar paquete JSON
    packet_json = json.dumps(packet, indent=2, default=str)
    with open('ternary_bimotype_packet.json', 'w') as f:
        f.write(packet_json)
    
    print("✓ Saved: ternary_bimotype_packet.json")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    demo_ternary_bimotype()
