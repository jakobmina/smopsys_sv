#!/usr/bin/env python3
"""
BiMoType Data Structures
========================

Define las estructuras de datos para el protocolo BiMoType
(Bi-Modal Type) de comunicación cuántica radiactiva.

Autor: Jacobo Tlacaelel Mina Rodriguez
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any


# ============================================================================
# ENUMERACIONES
# ============================================================================

class TipoDecaimiento(Enum):
    """Tipos de decaimiento radiactivo"""
    BETA = "BETA"      # β⁻ decay (electrón)
    GAMMA = "GAMMA"    # γ decay (fotón)
    ALPHA = "ALPHA"    # α decay (núcleo de helio)
    STABLE = "STABLE"  # Isótopo estable (sin decaimiento)
    
    def __str__(self):
        return self.value


# ============================================================================
# ESTRUCTURAS DE DATOS
# ============================================================================

@dataclass
class FirmaRadiactiva:
    """
    Firma radiactiva para protocolo BiMoType.
    
    Combina propiedades nucleares con métricas cuánticas
    para codificación de información.
    """
    
    # Identificación del isótopo
    isotope: str
    
    # Propiedades radiactivas
    decay_type: TipoDecaimiento
    energy_peak_ev: float          # Energía del pico (eV)
    half_life_s: float             # Vida media (segundos)
    nuclear_spin: float            # Spin nuclear
    
    # Métricas cuánticas (Mahalanobis-Gravedad)
    mahalanobis_distance: float    # Distancia de Mahalanobis
    lambda_double_non_locality: float  # λ de no-localidad doble
    mg_polarity: float             # Polaridad MG (0-1)
    mg_threshold: float = 0.5      # Umbral MG
    
    # Propiedades del vacío
    vacuum_polarity_n_r: float = 0.0  # Polaridad del vacío
    
    # Estado cuántico
    quantum_phase: float = 0.0     # Fase cuántica (radianes)
    
    # Codificación topológica (opcional)
    topology_encoding: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para serialización"""
        return {
            'isotope': self.isotope,
            'decay_type': str(self.decay_type),
            'energy_peak_ev': self.energy_peak_ev,
            'half_life_s': self.half_life_s,
            'nuclear_spin': self.nuclear_spin,
            'mahalanobis_distance': self.mahalanobis_distance,
            'lambda_double_non_locality': self.lambda_double_non_locality,
            'mg_polarity': self.mg_polarity,
            'mg_threshold': self.mg_threshold,
            'vacuum_polarity_n_r': self.vacuum_polarity_n_r,
            'quantum_phase': self.quantum_phase,
            'topology_encoding': self.topology_encoding
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FirmaRadiactiva':
        """Crea desde diccionario"""
        # Convertir string a enum
        if isinstance(data['decay_type'], str):
            data['decay_type'] = TipoDecaimiento(data['decay_type'])
        
        return cls(**data)


@dataclass
class EstadoCuantico:
    """
    Estado cuántico para un qubit en el protocolo BiMoType.
    
    Representa |ψ⟩ = α|0⟩ + β|1⟩
    """
    alpha: complex  # Amplitud del estado |0⟩
    beta: complex   # Amplitud del estado |1⟩
    
    def __post_init__(self):
        """Valida normalización"""
        norm = abs(self.alpha)**2 + abs(self.beta)**2
        if abs(norm - 1.0) > 1e-6:
            raise ValueError(f"Estado no normalizado: |α|² + |β|² = {norm}")
    
    @property
    def phase(self) -> float:
        """Calcula la fase relativa"""
        import cmath
        return cmath.phase(self.beta / self.alpha) if self.alpha != 0 else 0.0
    
    @property
    def probability_0(self) -> float:
        """Probabilidad de medir |0⟩"""
        return abs(self.alpha)**2
    
    @property
    def probability_1(self) -> float:
        """Probabilidad de medir |1⟩"""
        return abs(self.beta)**2
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        return {
            'alpha_real': self.alpha.real,
            'alpha_imag': self.alpha.imag,
            'beta_real': self.beta.real,
            'beta_imag': self.beta.imag,
            'phase': self.phase,
            'prob_0': self.probability_0,
            'prob_1': self.probability_1
        }


@dataclass
class PaqueteBiMoType:
    """
    Paquete completo del protocolo BiMoType.
    """
    packet_id: str
    protocol_version: str
    timestamp: float
    message: str
    quantum_states: list  # Lista de EstadoCuantico o dicts
    encoding_metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para JSON"""
        return {
            'packet_id': self.packet_id,
            'protocol_version': self.protocol_version,
            'timestamp': self.timestamp,
            'message': self.message,
            'quantum_states': [
                qs.to_dict() if hasattr(qs, 'to_dict') else qs
                for qs in self.quantum_states
            ],
            'encoding_metadata': self.encoding_metadata
        }


# ============================================================================
# CONSTANTES RADIACTIVAS
# ============================================================================

RADIOACTIVE_ISOTOPES = {
    'Sr90': {
        'name': 'Strontium-90',
        'Z': 38,
        'A': 90,
        'decay_type': TipoDecaimiento.BETA,
        'half_life_years': 28.8,
        'energy_ev': 546000.0,
        'spin': 0
    },
    'Tc99m': {
        'name': 'Technetium-99m',
        'Z': 43,
        'A': 99,
        'decay_type': TipoDecaimiento.GAMMA,
        'half_life_years': 0.25,
        'energy_ev': 140000.0,
        'spin': 9/2
    },
    'Pu238': {
        'name': 'Plutonium-238',
        'Z': 94,
        'A': 238,
        'decay_type': TipoDecaimiento.ALPHA,
        'half_life_years': 87.7,
        'energy_ev': 5590000.0,
        'spin': 0
    },
    'H1': {
        'name': 'Protio',
        'Z': 1,
        'A': 1,
        'decay_type': TipoDecaimiento.STABLE,
        'half_life_years': float('inf'),
        'energy_ev': 0.0,
        'spin': 1/2
    },
    'H2': {
        'name': 'Deuterio',
        'Z': 1,
        'A': 2,
        'decay_type': TipoDecaimiento.STABLE,
        'half_life_years': float('inf'),
        'energy_ev': 0.0,
        'spin': 1
    },
    'H3': {
        'name': 'Tritio',
        'Z': 1,
        'A': 3,
        'decay_type': TipoDecaimiento.BETA,
        'half_life_years': 12.32,
        'energy_ev': 18600.0, # Energía máxima beta (18.6 keV)
        'spin': 1/2
    }
}


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def crear_firma_desde_isotopo(isotope_name: str, **kwargs) -> FirmaRadiactiva:
    """
    Crea una FirmaRadiactiva desde un isótopo conocido.
    
    Args:
        isotope_name: Nombre del isótopo (e.g., 'Sr90')
        **kwargs: Parámetros adicionales para sobrescribir
    
    Returns:
        FirmaRadiactiva configurada
    """
    if isotope_name not in RADIOACTIVE_ISOTOPES:
        raise ValueError(f"Isótopo desconocido: {isotope_name}")
    
    iso_data = RADIOACTIVE_ISOTOPES[isotope_name]
    
    # Valores por defecto
    defaults = {
        'isotope': isotope_name,
        'decay_type': iso_data['decay_type'],
        'energy_peak_ev': iso_data['energy_ev'],
        'half_life_s': iso_data['half_life_years'] * 3.154e7 if iso_data['half_life_years'] != float('inf') else float('inf'),
        'nuclear_spin': iso_data['spin'],
        'mahalanobis_distance': 0.5,
        'lambda_double_non_locality': 0.5,
        'mg_polarity': 0.5,
        'mg_threshold': 0.5,
        'vacuum_polarity_n_r': 0.0,
        'quantum_phase': 0.0
    }
    
    # Sobrescribir con kwargs
    defaults.update(kwargs)
    
    return FirmaRadiactiva(**defaults)


if __name__ == '__main__':
    # Demo
    print("=" * 80)
    print("  BIMOTYPE DATA STRUCTURES DEMO")
    print("=" * 80)
    
    # Crear firma radiactiva
    firma = crear_firma_desde_isotopo(
        'Sr90',
        mahalanobis_distance=0.7,
        quantum_phase=1.57
    )
    
    print(f"\nFirma Radiactiva:")
    print(f"  Isótopo: {firma.isotope}")
    print(f"  Tipo: {firma.decay_type}")
    print(f"  Energía: {firma.energy_peak_ev} eV")
    print(f"  Vida media: {firma.half_life_s:.2e} s")
    print(f"  Fase cuántica: {firma.quantum_phase:.4f} rad")
    
    # Crear estado cuántico
    import numpy as np
    phase = np.pi / 4
    estado = EstadoCuantico(
        alpha=np.cos(phase/2),
        beta=np.sin(phase/2)
    )
    
    print(f"\nEstado Cuántico:")
    print(f"  α = {estado.alpha:.4f}")
    print(f"  β = {estado.beta:.4f}")
    print(f"  Fase = {estado.phase:.4f} rad")
    print(f"  P(|0⟩) = {estado.probability_0:.4f}")
    print(f"  P(|1⟩) = {estado.probability_1:.4f}")
    
    print("\n" + "=" * 80)
