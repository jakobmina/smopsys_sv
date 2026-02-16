#!/usr/bin/env python3
"""
Tests for BiMoType-Ternary Integration
=======================================

Tests de mapeo topológico, codificación/decodificación,
y generación de código C.

Autor: Jacobo Tlacaelel Mina Rodriguez
"""

import pytest
import numpy as np
import json
import sys
sys.path.insert(0, '..')

from bimotype_ternary_integration import (
    TopologyBiMoTypeMapper,
    TernaryBiMoTypeEncoder,
    TernaryBiMoTypeDecoder,
    TernaryBiMoTypeCodegen
)


class TestTopologyBiMoTypeMapper:
    """Tests del mapeador topología ↔ BiMoType"""
    
    def test_ternary_to_decay_type_mapping(self):
        """Test mapeo peso ternario → tipo de decaimiento"""
        assert TopologyBiMoTypeMapper.TERNARY_TO_DECAY_TYPE[-1] == 'BETA'
        assert TopologyBiMoTypeMapper.TERNARY_TO_DECAY_TYPE[0] == 'GAMMA'
        assert TopologyBiMoTypeMapper.TERNARY_TO_DECAY_TYPE[1] == 'ALPHA'
    
    def test_decay_to_isotope_mapping(self):
        """Test mapeo tipo de decaimiento → isótopo"""
        assert TopologyBiMoTypeMapper.DECAY_TO_ISOTOPE['BETA'] == 'Sr90'
        assert TopologyBiMoTypeMapper.DECAY_TO_ISOTOPE['GAMMA'] == 'Tc99m'
        assert TopologyBiMoTypeMapper.DECAY_TO_ISOTOPE['ALPHA'] == 'Pu238'
    
    def test_h7_index_to_phase(self):
        """Test conversión H7 → fase cuántica"""
        assert TopologyBiMoTypeMapper.h7_index_to_phase(0) == pytest.approx(0.0)
        assert TopologyBiMoTypeMapper.h7_index_to_phase(7) == pytest.approx(2 * np.pi)
        assert TopologyBiMoTypeMapper.h7_index_to_phase(3) == pytest.approx(3 * np.pi / 3.5)
    
    def test_chirality_to_mg_polarity(self):
        """Test conversión quiralidad → polaridad MG"""
        assert TopologyBiMoTypeMapper.chirality_to_mg_polarity(-1.0) == pytest.approx(0.0)
        assert TopologyBiMoTypeMapper.chirality_to_mg_polarity(0.0) == pytest.approx(0.5)
        assert TopologyBiMoTypeMapper.chirality_to_mg_polarity(1.0) == pytest.approx(1.0)
    
    def test_create_radioactive_signature_beta(self):
        """Test creación de firma radiactiva para BETA decay"""
        topology_state = {
            'indice': 2,
            'pareja': 5,
            'winding': 2,
            'mapeo': 1,
            'peso_ternario': -1,  # BETA
            'fase_discreta_fragmento': 2
        }
        
        sig = TopologyBiMoTypeMapper.create_radioactive_signature_from_topology(topology_state)
        
        assert sig['isotope'] == 'Sr90'
        assert 'quantum_phase' in sig
        assert 'mg_polarity' in sig
    
    def test_create_radioactive_signature_gamma(self):
        """Test creación de firma radiactiva para GAMMA decay"""
        topology_state = {
            'indice': 3,
            'pareja': 4,
            'winding': 0,
            'mapeo': 0,
            'peso_ternario': 0,  # GAMMA
            'fase_discreta_fragmento': 3
        }
        
        sig = TopologyBiMoTypeMapper.create_radioactive_signature_from_topology(topology_state)
        
        assert sig['isotope'] == 'Tc99m'
    
    def test_create_radioactive_signature_alpha(self):
        """Test creación de firma radiactiva para ALPHA decay"""
        topology_state = {
            'indice': 1,
            'pareja': 6,
            'winding': 0,
            'mapeo': 0,
            'peso_ternario': 1,  # ALPHA
            'fase_discreta_fragmento': 0
        }
        
        sig = TopologyBiMoTypeMapper.create_radioactive_signature_from_topology(topology_state)
        
        assert sig['isotope'] == 'Pu238'


class TestTernaryBiMoTypeEncoder:
    """Tests del codificador ternario-BiMoType"""
    
    def test_encode_single_character(self):
        """Test codificación de un solo carácter"""
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology("A", use_nuclear_isotopes=False)
        
        assert encoded['message'] == "A"
        assert len(encoded['encoded_characters']) == 1
        assert encoded['encoding_method'] == 'Ternary-BiMoType-Hybrid'
    
    def test_encode_hello(self):
        """Test codificación de 'HELLO'"""
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology("HELLO", use_nuclear_isotopes=False)
        
        assert encoded['message'] == "HELLO"
        assert len(encoded['encoded_characters']) == 5
        
        # Verificar que cada carácter tiene los campos requeridos
        for char_enc in encoded['encoded_characters']:
            assert 'character' in char_enc
            assert 'topology_state' in char_enc
            assert 'radioactive_signature' in char_enc
            assert 'hex_encoding' in char_enc
    
    def test_create_bimotype_packet(self):
        """Test creación de paquete BiMoType"""
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology("TEST", use_nuclear_isotopes=False)
        packet = encoder.create_bimotype_packet_from_ternary(encoded)
        
        assert 'packet_id' in packet
        assert 'protocol' in packet
        assert packet['protocol'] == 'Ternary-BiMoType-v1.0'
        assert packet['message'] == "TEST"
        assert len(packet['quantum_states']) == 4
        
        # Verificar estructura de estados cuánticos
        for qs in packet['quantum_states']:
            assert 'alpha' in qs
            assert 'beta' in qs
            assert 'phase' in qs
            assert 'isotope' in qs
            assert 'decay_type' in qs
    
    def test_quantum_state_normalization(self):
        """Test normalización de estados cuánticos"""
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology("X", use_nuclear_isotopes=False)
        packet = encoder.create_bimotype_packet_from_ternary(encoded)
        
        for qs in packet['quantum_states']:
            # |α|² + |β|² = 1
            norm = qs['alpha']**2 + qs['beta']**2
            assert norm == pytest.approx(1.0, abs=1e-6)
    
    def test_decay_types_distribution(self):
        """Test distribución de tipos de decaimiento"""
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology("ABCDEF", use_nuclear_isotopes=False)
        packet = encoder.create_bimotype_packet_from_ternary(encoded)
        
        dist = packet['encoding_metadata']['decay_types_distribution']
        
        # Debe haber al menos un tipo de decaimiento
        assert len(dist) > 0
        
        # La suma debe ser igual al número de caracteres
        assert sum(dist.values()) == 6


class TestTernaryBiMoTypeDecoder:
    """Tests del decodificador ternario-BiMoType"""
    
    def test_decode_without_noise(self):
        """Test decodificación sin ruido"""
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology("HELLO", use_nuclear_isotopes=False)
        packet = encoder.create_bimotype_packet_from_ternary(encoded)
        
        decoder = TernaryBiMoTypeDecoder()
        decoded = decoder.decode_bimotype_packet(packet, noise_level=0.0)
        
        assert decoded['decoded_message'] == "HELLO"
        assert decoded['original_message'] == "HELLO"
        assert decoded['average_fidelity'] > 0.99
        assert decoded['decoding_quality'] == 'EXCELLENT'
    
    def test_decode_with_low_noise(self):
        """Test decodificación con ruido bajo"""
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology("TEST", use_nuclear_isotopes=False)
        packet = encoder.create_bimotype_packet_from_ternary(encoded)
        
        decoder = TernaryBiMoTypeDecoder()
        decoded = decoder.decode_bimotype_packet(packet, noise_level=0.1)
        
        # Con ruido bajo, la fidelidad debe ser alta
        assert decoded['average_fidelity'] > 0.85
        assert decoded['decoding_quality'] in ['EXCELLENT', 'GOOD']
    
    
    def test_fidelity_calculation(self):
        """Test cálculo de fidelidad"""
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology("A", use_nuclear_isotopes=False)
        packet = encoder.create_bimotype_packet_from_ternary(encoded)
        
        decoder = TernaryBiMoTypeDecoder()
        decoded = decoder.decode_bimotype_packet(packet, noise_level=0.0)
        
        # Fidelidad debe estar entre 0 y 1
        assert 0.0 <= decoded['average_fidelity'] <= 1.0
        assert len(decoded['character_fidelities']) == 1


class TestTernaryBiMoTypeCodegen:
    """Tests del generador de código C"""
    
    def test_generate_header(self):
        """Test generación de header C"""
        codegen = TernaryBiMoTypeCodegen()
        header = codegen.generate_header()
        
        # Verificar que contiene elementos clave
        assert '#ifndef TERNARY_BIMOTYPE_H' in header
        assert '#define TERNARY_BIMOTYPE_H' in header
        assert 'typedef enum' in header
        assert 'DecayType' in header
        assert 'TernaryRadioactiveSignature' in header
        assert 'TernaryQuantumState' in header
    
    def test_header_has_required_functions(self):
        """Test que el header tiene funciones requeridas"""
        codegen = TernaryBiMoTypeCodegen()
        header = codegen.generate_header()
        
        assert 'ternary_to_decay_type' in header
        assert 'decay_type_to_isotope' in header
        assert 'h7_index_to_phase' in header
        assert 'chirality_to_mg_polarity' in header
        assert 'topology_pack' in header
        assert 'create_radioactive_signature_from_topology' in header
        assert 'create_quantum_state_from_signature' in header
    
    def test_header_has_isotope_names(self):
        """Test que el header contiene nombres de isótopos"""
        codegen = TernaryBiMoTypeCodegen()
        header = codegen.generate_header()
        
        assert 'Sr90' in header
        assert 'Tc99m' in header
        assert 'Pu238' in header


class TestIntegrationEndToEnd:
    """Tests de integración end-to-end"""
    
    def test_full_pipeline(self):
        """Test pipeline completo: encode → packet → decode"""
        message = "QUANTUM"
        
        # Encode
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology(message, use_nuclear_isotopes=False)
        
        # Create packet
        packet = encoder.create_bimotype_packet_from_ternary(encoded)
        
        # Decode
        decoder = TernaryBiMoTypeDecoder()
        decoded = decoder.decode_bimotype_packet(packet, noise_level=0.05)
        
        # Verify
        assert decoded['original_message'] == message
        assert decoded['average_fidelity'] > 0.90
    
    def test_json_serialization(self):
        """Test serialización JSON del paquete"""
        encoder = TernaryBiMoTypeEncoder()
        encoded = encoder.encode_message_with_topology("JSON", use_nuclear_isotopes=False)
        packet = encoder.create_bimotype_packet_from_ternary(encoded)
        
        # Serializar
        json_str = json.dumps(packet, default=str)
        
        # Deserializar
        recovered = json.loads(json_str)
        
        assert recovered['message'] == "JSON"
        assert len(recovered['quantum_states']) == 4
    
    def test_multiple_messages(self):
        """Test codificación de múltiples mensajes"""
        messages = ["A", "AB", "ABC", "ABCD", "ABCDE"]
        
        encoder = TernaryBiMoTypeEncoder()
        decoder = TernaryBiMoTypeDecoder()
        
        for msg in messages:
            encoded = encoder.encode_message_with_topology(msg, use_nuclear_isotopes=False)
            packet = encoder.create_bimotype_packet_from_ternary(encoded)
            decoded = decoder.decode_bimotype_packet(packet, noise_level=0.1)
            
            assert decoded['original_message'] == msg
            assert decoded['average_fidelity'] > 0.80


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
