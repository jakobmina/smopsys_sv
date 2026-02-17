#!/usr/bin/env python3
"""
Quantum Crypto CLI
==================

Command-line interface for quantum password generation and encryption.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

import click
import sys

from .password_generator import QuantumPasswordGenerator
from .encryptor import QuantumEncryptor, EncryptedPacket


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    BiMoType Quantum Cryptography CLI
    
    Generate secure passwords and encrypt data using quantum topology.
    """
    pass


@cli.command()
@click.option('--length', '-l', default=16, help='Password length')
@click.option('--charset', '-c', default='alphanumeric+symbols',
              type=click.Choice([
                  'lowercase', 'uppercase', 'digits', 'symbols',
                  'alphanumeric', 'alphanumeric+symbols', 'all'
              ]),
              help='Character set')
@click.option('--count', '-n', default=1, help='Number of passwords to generate')
@click.option('--analyze', '-a', is_flag=True, help='Show strength analysis')
def password(length, charset, count, analyze):
    """Generate quantum-secure passwords"""
    try:
        gen = QuantumPasswordGenerator()
        
        for i in range(count):
            pwd = gen.generate(length=length, charset=charset)
            
            if analyze:
                analysis = gen.analyze_strength(pwd)
                click.echo(f"\nPassword {i+1}: {pwd}")
                click.echo(f"  Length: {analysis['length']}")
                click.echo(f"  Charset size: {analysis['charset_size']}")
                click.echo(f"  Theoretical entropy: {analysis['theoretical_entropy_bits']:.2f} bits")
                click.echo(f"  Actual entropy: {analysis['actual_entropy_bits']:.2f} bits")
                click.echo(f"  Strength: {analysis['strength']}")
            else:
                click.echo(pwd)
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--input', '-i', 'input_file', required=True, help='Input file to encrypt')
@click.option('--output', '-o', 'output_file', required=True, help='Output encrypted file')
@click.option('--password', '-p', prompt=True, hide_input=True, confirmation_prompt=True,
              help='Encryption password')
def encrypt(input_file, output_file, password):
    """Encrypt a file using quantum-derived keys"""
    try:
        encryptor = QuantumEncryptor()
        
        click.echo(f"Encrypting {input_file}...")
        encryptor.encrypt_file(input_file, output_file, password)
        
        # Load packet to show metadata
        with open(output_file, 'r') as f:
            import json
            packet_data = json.load(f)
        
        click.echo(f"✓ Encrypted to {output_file}")
        click.echo(f"\nQuantum Metadata:")
        click.echo(f"  Isotope: {packet_data['metadata']['isotope']}")
        click.echo(f"  Decay type: {packet_data['metadata']['decay_type']}")
        click.echo(f"  H7 index: {packet_data['metadata']['h7_index']}")
        click.echo(f"  Quantum phase: {packet_data['metadata']['quantum_phase']:.4f} rad")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--input', '-i', 'input_file', required=True, help='Input encrypted file')
@click.option('--output', '-o', 'output_file', required=True, help='Output decrypted file')
@click.option('--password', '-p', prompt=True, hide_input=True, help='Decryption password')
def decrypt(input_file, output_file, password):
    """Decrypt a file"""
    try:
        encryptor = QuantumEncryptor()
        
        click.echo(f"Decrypting {input_file}...")
        encryptor.decrypt_file(input_file, output_file, password)
        
        click.echo(f"✓ Decrypted to {output_file}")
        
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('password')
def entropy(password):
    """Analyze password entropy and strength"""
    try:
        gen = QuantumPasswordGenerator()
        analysis = gen.analyze_strength(password)
        
        click.echo(f"\nPassword Analysis:")
        click.echo(f"  Password: {'*' * len(password)}")
        click.echo(f"  Length: {analysis['length']}")
        click.echo(f"  Has lowercase: {analysis['has_lowercase']}")
        click.echo(f"  Has uppercase: {analysis['has_uppercase']}")
        click.echo(f"  Has digits: {analysis['has_digits']}")
        click.echo(f"  Has symbols: {analysis['has_symbols']}")
        click.echo(f"  Charset size: {analysis['charset_size']}")
        click.echo(f"  Theoretical entropy: {analysis['theoretical_entropy_bits']:.2f} bits")
        click.echo(f"  Actual entropy: {analysis['actual_entropy_bits']:.2f} bits")
        click.echo(f"  Strength: {analysis['strength']}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
