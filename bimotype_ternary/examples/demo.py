#!/usr/bin/env python3
"""
BiMoType-Ternary Demo
=====================

Demonstrates the complete integration pipeline.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

import json
from bimotype_ternary import (
    TernaryBiMoTypeEncoder,
    TernaryBiMoTypeDecoder,
    TernaryBiMoTypeCodegen
)


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
    
    encoded = encoder.encode_message_with_topology(message, use_nuclear_isotopes=False)
    
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
