import pytest
import numpy as np
from datatypes import TipoDecaimiento, FirmaRadiactiva, EstadoCuantico, PaqueteBiMoType, crear_firma_desde_isotopo

def test_tipo_decaimiento_str():
    assert str(TipoDecaimiento.BETA) == "BETA"
    assert str(TipoDecaimiento.GAMMA) == "GAMMA"

def test_firma_radiactiva_creation():
    firma = FirmaRadiactiva(
        isotope="Sr90",
        decay_type=TipoDecaimiento.BETA,
        energy_peak_ev=0.546,
        half_life_s=9.08e8,
        nuclear_spin=0,
        mahalanobis_distance=0.7,
        lambda_double_non_locality=0.5,
        mg_polarity=0.8
    )
    assert firma.isotope == "Sr90"
    assert firma.mg_polarity == 0.8
    
    d = firma.to_dict()
    assert d['isotope'] == "Sr90"
    assert d['decay_type'] == "BETA"

def test_estado_cuantico_normalization():
    # Valid normalization
    estado = EstadoCuantico(alpha=1/np.sqrt(2), beta=1/np.sqrt(2))
    assert pytest.approx(estado.probability_0 + estado.probability_1) == 1.0
    
    # Invalid normalization should raise ValueError
    with pytest.raises(ValueError):
        EstadoCuantico(alpha=1.0, beta=1.0)

def test_crear_firma_desde_isotopo():
    firma = crear_firma_desde_isotopo("Sr90")
    assert firma.isotope == "Sr90"
    assert firma.decay_type == TipoDecaimiento.BETA
    
    # Test Tritium
    h3 = crear_firma_desde_isotopo("H3")
    assert h3.isotope == "H3"
    assert h3.decay_type == TipoDecaimiento.BETA
    assert h3.energy_peak_ev == 0.0186
    
    # Test Protium (Stable)
    h1 = crear_firma_desde_isotopo("H1")
    assert h1.isotope == "H1"
    assert h1.decay_type == TipoDecaimiento.STABLE
    assert h1.energy_peak_ev == 0.0
    
    with pytest.raises(ValueError):
        crear_firma_desde_isotopo("IsotopoInexistente")

def test_paquete_bimo_type():
    estado = EstadoCuantico(alpha=1.0, beta=0.0)
    paquete = PaqueteBiMoType(
        packet_id="test-123",
        protocol_version="1.0",
        timestamp=123456789.0,
        message="Hello",
        quantum_states=[estado],
        encoding_metadata={"test": True}
    )
    assert paquete.packet_id == "test-123"
    assert len(paquete.quantum_states) == 1
    
    d = paquete.to_dict()
    assert d['quantum_states'][0]['prob_0'] == 1.0
