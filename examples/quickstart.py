#!/usr/bin/env python3
"""
Quick Start Example
===================

Basic usage of BiMoType-Ternary framework.
"""

from bimotype_ternary import (
    TernaryBiMoTypeEncoder,
    TernaryBiMoTypeDecoder
)


def main():
    # 1. Encode a message
    encoder = TernaryBiMoTypeEncoder()
    encoded = encoder.encode_message_with_topology("QUANTUM")
    packet = encoder.create_bimotype_packet_from_ternary(encoded)
    
    print(f"Packet ID: {packet['packet_id']}")
    print(f"Total Energy: {packet['encoding_metadata']['total_energy_ev']:.3f} eV")
    
    # 2. Decode with noise simulation
    decoder = TernaryBiMoTypeDecoder()
    decoded = decoder.decode_bimotype_packet(packet, noise_level=0.1)
    
    print(f"\nOriginal:  {decoded['original_message']}")
    print(f"Decoded:   {decoded['decoded_message']}")
    print(f"Fidelity:  {decoded['average_fidelity']:.4f}")
    print(f"Quality:   {decoded['decoding_quality']}")


if __name__ == '__main__':
    main()
