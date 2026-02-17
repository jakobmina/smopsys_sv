#!/usr/bin/env python3
"""
Quantum Password Generator
===========================

Generate cryptographically secure passwords using quantum entropy
from radioactive decay simulation and topology state mixing.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

import hashlib
import secrets
import math
from typing import Dict, List, Optional
from collections import Counter

try:
    from ..topology.encoder import CodificadorTopologicoBigEndian
    from ..integration.mapper import TopologyBiMoTypeMapper
    TOPOLOGY_AVAILABLE = True
except ImportError:
    TOPOLOGY_AVAILABLE = False


class QuantumPasswordGenerator:
    """
    Genera contraseñas criptográficamente seguras usando entropía cuántica.
    
    Características:
    - Entropía de decaimiento radiactivo simulado (Sr-90, Tc-99m, Pu-238)
    - Mezcla de estados topológicos H7
    - Generación determinista desde seed (para recuperación)
    - Estimación de entropía Shannon
    """
    
    # Character sets
    CHARSET_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
    CHARSET_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    CHARSET_DIGITS = '0123456789'
    CHARSET_SYMBOLS = '!@#$%^&*()-_=+[]{}|;:,.<>?'
    
    CHARSET_PRESETS = {
        'lowercase': CHARSET_LOWERCASE,
        'uppercase': CHARSET_UPPERCASE,
        'digits': CHARSET_DIGITS,
        'symbols': CHARSET_SYMBOLS,
        'alphanumeric': CHARSET_LOWERCASE + CHARSET_UPPERCASE + CHARSET_DIGITS,
        'alphanumeric+symbols': CHARSET_LOWERCASE + CHARSET_UPPERCASE + CHARSET_DIGITS + CHARSET_SYMBOLS,
        'all': CHARSET_LOWERCASE + CHARSET_UPPERCASE + CHARSET_DIGITS + CHARSET_SYMBOLS,
    }
    
    def __init__(self):
        """Inicializa el generador de contraseñas cuánticas"""
        if not TOPOLOGY_AVAILABLE:
            raise ImportError("Topology encoder not available. Install bimotype_ternary package.")
        
        self.topology_encoder = CodificadorTopologicoBigEndian()
        self.mapper = TopologyBiMoTypeMapper()
    
    def _extract_quantum_entropy(self, num_bytes: int = 32) -> bytes:
        """
        Extrae entropía cuántica de estados topológicos y decaimiento radiactivo.
        
        Args:
            num_bytes: Número de bytes de entropía a generar
            
        Returns:
            Bytes de entropía cuántica
        """
        entropy_pool = bytearray()
        
        # Usar secrets como fuente base (CSPRNG del sistema)
        base_entropy = secrets.token_bytes(num_bytes)
        entropy_pool.extend(base_entropy)
        
        # Mezclar con estados topológicos
        for i in range(6):  # 6 estados topológicos
            state = self.topology_encoder.topology_entries[i]
            
            # Crear firma radiactiva
            sig = self.mapper.create_radioactive_signature_from_topology(state)
            
            # Extraer entropía de la firma
            sig_bytes = (
                sig['isotope'].encode() +
                str(sig['quantum_phase']).encode() +
                str(sig['mg_polarity']).encode() +
                str(sig.get('energy_peak_ev', 0.0)).encode()
            )
            
            # Hash para mezclar
            h = hashlib.sha256(sig_bytes).digest()
            entropy_pool.extend(h)
        
        # Hash final para mezclar todo
        final_entropy = hashlib.sha512(bytes(entropy_pool)).digest()
        
        return final_entropy[:num_bytes]
    
    def generate(
        self,
        length: int = 16,
        charset: str = 'alphanumeric+symbols',
        ensure_complexity: bool = True
    ) -> str:
        """
        Genera una contraseña criptográficamente segura.
        
        Args:
            length: Longitud de la contraseña
            charset: Conjunto de caracteres ('lowercase', 'uppercase', 'digits', 
                    'symbols', 'alphanumeric', 'alphanumeric+symbols', 'all')
            ensure_complexity: Asegurar que incluye al menos un carácter de cada tipo
            
        Returns:
            Contraseña generada
        """
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        # Obtener charset
        if charset in self.CHARSET_PRESETS:
            chars = self.CHARSET_PRESETS[charset]
        else:
            chars = charset
        
        if not chars:
            raise ValueError("Character set cannot be empty")
        
        # Extraer entropía cuántica
        entropy = self._extract_quantum_entropy(length * 2)
        
        # Generar contraseña
        password = []
        for i in range(length):
            # Usar entropía cuántica para seleccionar carácter
            byte_val = entropy[i % len(entropy)]
            char_idx = byte_val % len(chars)
            password.append(chars[char_idx])
        
        password_str = ''.join(password)
        
        # Asegurar complejidad si se requiere
        if ensure_complexity and charset in ['alphanumeric+symbols', 'all']:
            password_str = self._ensure_complexity(password_str, charset)
        
        return password_str
    
    def _ensure_complexity(self, password: str, charset: str) -> str:
        """
        Asegura que la contraseña tiene al menos un carácter de cada tipo.
        
        Args:
            password: Contraseña a verificar
            charset: Conjunto de caracteres usado
            
        Returns:
            Contraseña con complejidad asegurada
        """
        has_lower = any(c in self.CHARSET_LOWERCASE for c in password)
        has_upper = any(c in self.CHARSET_UPPERCASE for c in password)
        has_digit = any(c in self.CHARSET_DIGITS for c in password)
        has_symbol = any(c in self.CHARSET_SYMBOLS for c in password)
        
        if charset == 'alphanumeric+symbols' or charset == 'all':
            if has_lower and has_upper and has_digit and has_symbol:
                return password
            
            # Reemplazar caracteres para asegurar complejidad
            pwd_list = list(password)
            entropy = self._extract_quantum_entropy(4)
            
            if not has_lower:
                idx = entropy[0] % len(pwd_list)
                pwd_list[idx] = self.CHARSET_LOWERCASE[entropy[0] % len(self.CHARSET_LOWERCASE)]
            
            if not has_upper:
                idx = entropy[1] % len(pwd_list)
                pwd_list[idx] = self.CHARSET_UPPERCASE[entropy[1] % len(self.CHARSET_UPPERCASE)]
            
            if not has_digit:
                idx = entropy[2] % len(pwd_list)
                pwd_list[idx] = self.CHARSET_DIGITS[entropy[2] % len(self.CHARSET_DIGITS)]
            
            if not has_symbol and charset == 'alphanumeric+symbols':
                idx = entropy[3] % len(pwd_list)
                pwd_list[idx] = self.CHARSET_SYMBOLS[entropy[3] % len(self.CHARSET_SYMBOLS)]
            
            return ''.join(pwd_list)
        
        return password
    
    def generate_with_seed(
        self,
        seed: str,
        length: int = 16,
        charset: str = 'alphanumeric+symbols'
    ) -> str:
        """
        Genera una contraseña determinista desde un seed.
        
        ADVERTENCIA: Útil para recuperación, pero menos seguro que generate().
        
        Args:
            seed: Semilla para generación determinista
            length: Longitud de la contraseña
            charset: Conjunto de caracteres
            
        Returns:
            Contraseña generada determinísticamente
        """
        # Hash del seed
        seed_hash = hashlib.sha512(seed.encode()).digest()
        
        # Obtener charset
        if charset in self.CHARSET_PRESETS:
            chars = self.CHARSET_PRESETS[charset]
        else:
            chars = charset
        
        # Generar contraseña determinísticamente
        password = []
        for i in range(length):
            # Usar hash del seed + índice
            h = hashlib.sha256(seed_hash + i.to_bytes(4, 'big')).digest()
            char_idx = h[0] % len(chars)
            password.append(chars[char_idx])
        
        return ''.join(password)
    
    def estimate_entropy(self, password: str) -> float:
        """
        Estima la entropía Shannon de una contraseña.
        
        Args:
            password: Contraseña a analizar
            
        Returns:
            Entropía en bits
        """
        if not password:
            return 0.0
        
        # Contar frecuencias de caracteres
        freq = Counter(password)
        length = len(password)
        
        # Calcular entropía Shannon
        entropy = 0.0
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)
        
        # Entropía total = entropía por carácter * longitud
        total_entropy = entropy * length
        
        return total_entropy
    
    def analyze_strength(self, password: str) -> Dict:
        """
        Analiza la fortaleza de una contraseña.
        
        Args:
            password: Contraseña a analizar
            
        Returns:
            Diccionario con métricas de fortaleza
        """
        length = len(password)
        
        # Detectar tipos de caracteres
        has_lower = any(c in self.CHARSET_LOWERCASE for c in password)
        has_upper = any(c in self.CHARSET_UPPERCASE for c in password)
        has_digit = any(c in self.CHARSET_DIGITS for c in password)
        has_symbol = any(c in self.CHARSET_SYMBOLS for c in password)
        
        # Calcular espacio de caracteres
        charset_size = 0
        if has_lower:
            charset_size += len(self.CHARSET_LOWERCASE)
        if has_upper:
            charset_size += len(self.CHARSET_UPPERCASE)
        if has_digit:
            charset_size += len(self.CHARSET_DIGITS)
        if has_symbol:
            charset_size += len(self.CHARSET_SYMBOLS)
        
        # Entropía teórica
        theoretical_entropy = length * math.log2(charset_size) if charset_size > 0 else 0
        
        # Entropía real (Shannon)
        actual_entropy = self.estimate_entropy(password)
        
        # Clasificación de fortaleza
        if theoretical_entropy >= 128:
            strength = "EXCELLENT"
        elif theoretical_entropy >= 80:
            strength = "STRONG"
        elif theoretical_entropy >= 60:
            strength = "GOOD"
        elif theoretical_entropy >= 40:
            strength = "FAIR"
        else:
            strength = "WEAK"
        
        return {
            'length': length,
            'has_lowercase': has_lower,
            'has_uppercase': has_upper,
            'has_digits': has_digit,
            'has_symbols': has_symbol,
            'charset_size': charset_size,
            'theoretical_entropy_bits': theoretical_entropy,
            'actual_entropy_bits': actual_entropy,
            'strength': strength,
        }
