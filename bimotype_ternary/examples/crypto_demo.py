#!/usr/bin/env python3
"""
Quantum Crypto Demo
===================

Demonstrates quantum password generation and encryption.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

from bimotype_ternary.crypto import (
    QuantumPasswordGenerator,
    QuantumKeyDerivation,
    QuantumEncryptor
)


def demo_password_generation():
    """Demo de generación de contraseñas"""
    print("=" * 80)
    print("  QUANTUM PASSWORD GENERATION")
    print("=" * 80)
    
    gen = QuantumPasswordGenerator()
    
    # Generar contraseñas con diferentes configuraciones
    configs = [
        ('lowercase', 12),
        ('alphanumeric', 16),
        ('alphanumeric+symbols', 24),
        ('all', 32),
    ]
    
    for charset, length in configs:
        password = gen.generate(length=length, charset=charset)
        analysis = gen.analyze_strength(password)
        
        print(f"\nCharset: {charset}, Length: {length}")
        print(f"  Password: {password}")
        print(f"  Entropy: {analysis['theoretical_entropy_bits']:.2f} bits")
        print(f"  Strength: {analysis['strength']}")


def demo_key_derivation():
    """Demo de derivación de claves"""
    print("\n" + "=" * 80)
    print("  QUANTUM KEY DERIVATION")
    print("=" * 80)
    
    kdf = QuantumKeyDerivation()
    
    password = "MySecretPassword123!"
    
    # Derivar clave con topología
    key = kdf.derive_key(password, iterations=10000, key_length=32)
    print(f"\nDerived key (hex): {key.hex()[:64]}...")
    
    # Derivar con H7 conservation
    for h7_idx in [0, 3, 7]:
        key_h7 = kdf.derive_key_with_h7_conservation(
            password,
            h7_index=h7_idx,
            iterations=10000
        )
        print(f"H7[{h7_idx}] key: {key_h7.hex()[:32]}...")


def demo_encryption():
    """Demo de encriptación"""
    print("\n" + "=" * 80)
    print("  QUANTUM ENCRYPTION")
    print("=" * 80)
    
    encryptor = QuantumEncryptor(iterations=10000)
    
    # Datos a encriptar
    plaintext = b"This is a secret quantum message!"
    password = "QuantumPassword2024!"
    
    print(f"\nPlaintext: {plaintext.decode()}")
    print(f"Password: {'*' * len(password)}")
    
    # Encriptar
    packet = encryptor.encrypt(plaintext, password)
    
    print(f"\nEncrypted packet:")
    print(f"  Ciphertext: {packet.ciphertext[:64]}...")
    print(f"  Nonce: {packet.nonce}")
    print(f"  Isotope: {packet.metadata['isotope']}")
    print(f"  Decay type: {packet.metadata['decay_type']}")
    print(f"  H7 index: {packet.metadata['h7_index']}")
    print(f"  Quantum phase: {packet.metadata['quantum_phase']:.4f} rad")
    
    # Verificar firma
    is_valid = encryptor.verify_signature(packet)
    print(f"  Signature valid: {is_valid}")
    
    # Desencriptar
    decrypted = encryptor.decrypt(packet, password)
    print(f"\nDecrypted: {decrypted.decode()}")
    
    # Verificar
    assert decrypted == plaintext
    print("✓ Encryption/decryption successful!")
    
    # Intentar con contraseña incorrecta
    try:
        encryptor.decrypt(packet, "WrongPassword")
        print("✗ Should have failed with wrong password!")
    except ValueError as e:
        print(f"✓ Wrong password detected: {e}")


def demo_file_encryption():
    """Demo de encriptación de archivos"""
    print("\n" + "=" * 80)
    print("  FILE ENCRYPTION")
    print("=" * 80)
    
    import tempfile
    import os
    
    encryptor = QuantumEncryptor(iterations=10000)
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Secret file content\nWith multiple lines\n[LOCKED]")
        temp_file = f.name
    
    encrypted_file = temp_file + '.enc'
    decrypted_file = temp_file + '.dec'
    
    password = "FilePassword123!"
    
    try:
        # Encriptar archivo
        print(f"\nEncrypting {os.path.basename(temp_file)}...")
        encryptor.encrypt_file(temp_file, encrypted_file, password)
        print(f"✓ Encrypted to {os.path.basename(encrypted_file)}")
        
        # Desencriptar archivo
        print(f"\nDecrypting {os.path.basename(encrypted_file)}...")
        encryptor.decrypt_file(encrypted_file, decrypted_file, password)
        print(f"✓ Decrypted to {os.path.basename(decrypted_file)}")
        
        # Verificar contenido
        with open(temp_file, 'r') as f:
            original = f.read()
        
        with open(decrypted_file, 'r') as f:
            recovered = f.read()
        
        assert original == recovered
        print("✓ File content verified!")
        
    finally:
        # Limpiar archivos temporales
        for path in [temp_file, encrypted_file, decrypted_file]:
            if os.path.exists(path):
                os.remove(path)


def main():
    """Ejecuta todos los demos"""
    demo_password_generation()
    demo_key_derivation()
    demo_encryption()
    demo_file_encryption()
    
    print("\n" + "=" * 80)
    print("  DEMO COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
