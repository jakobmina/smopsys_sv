#!/usr/bin/env python3
"""
Quantum Encryptor
=================

Encrypt/decrypt data using quantum-derived keys with AES-256-GCM.

Author: Jacobo Tlacaelel Mina Rodriguez
"""

import os
import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, Optional

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.exceptions import InvalidTag
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    from ..topology.encoder import CodificadorTopologicoBigEndian
    from ..integration.mapper import TopologyBiMoTypeMapper
    from .key_derivation import QuantumKeyDerivation
    TOPOLOGY_AVAILABLE = True
except ImportError:
    TOPOLOGY_AVAILABLE = False


@dataclass
class EncryptedPacket:
    """
    Paquete de datos encriptados con metadata cuántica.
    
    Attributes:
        ciphertext: Datos encriptados (base64)
        nonce: Nonce para AES-GCM (base64)
        salt: Salt usado para derivación de clave (base64)
        metadata: Metadata cuántica (isotope, h7_index, phase, etc.)
        timestamp: Timestamp de creación
        version: Versión del protocolo
    """
    ciphertext: str  # base64
    nonce: str  # base64
    salt: str  # base64
    metadata: Dict
    timestamp: float
    version: str = "QuantumCrypto-v1.0"
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convierte a JSON"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EncryptedPacket':
        """Crea desde diccionario"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'EncryptedPacket':
        """Crea desde JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)


class QuantumEncryptor:
    """
    Encripta/desencripta datos usando claves derivadas cuánticamente.
    
    Características:
    - AES-256-GCM para encriptación autenticada
    - Claves derivadas con PBKDF2 + topología cuántica
    - Nonce generado desde fase cuántica
    - Metadata: firma isotópica, índice H7, polaridad MG
    - Verificación de autenticidad
    """
    
    def __init__(self, iterations: int = 100000):
        """
        Inicializa el encriptador cuántico.
        
        Args:
            iterations: Número de iteraciones PBKDF2
        """
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library not available. Install with: pip install cryptography")
        
        if not TOPOLOGY_AVAILABLE:
            raise ImportError("Topology encoder not available")
        
        self.iterations = iterations
        self.key_derivation = QuantumKeyDerivation()
        self.topology_encoder = CodificadorTopologicoBigEndian()
        self.mapper = TopologyBiMoTypeMapper()
    
    def _generate_nonce_from_topology(self, password: str) -> bytes:
        """
        Genera un nonce único desde estados topológicos.
        
        Args:
            password: Contraseña para derivar nonce
            
        Returns:
            Nonce de 12 bytes (recomendado para AES-GCM)
        """
        # Usar timestamp + password para unicidad
        timestamp = str(time.time()).encode()
        nonce_seed = password.encode() + timestamp
        
        # Extraer entropía de topología
        salt = self.key_derivation._create_topology_salt(password)
        
        # Combinar y hash
        nonce_material = nonce_seed + salt
        
        # Usar os.urandom para seguridad adicional
        system_random = os.urandom(12)
        
        # XOR para mezclar
        nonce = bytes(a ^ b for a, b in zip(system_random, nonce_material[:12]))
        
        return nonce
    
    def _create_quantum_metadata(self, password: str, salt: bytes) -> Dict:
        """
        Crea metadata cuántica para el paquete encriptado.
        
        Args:
            password: Contraseña usada
            salt: Salt usado
            
        Returns:
            Diccionario con metadata cuántica
        """
        # Seleccionar estado topológico basado en password
        import hashlib
        pwd_hash = hashlib.sha256(password.encode()).digest()
        state_idx = pwd_hash[0] % 6
        
        state = self.topology_encoder.ESTADOS_TOPOLOGICOS[state_idx]
        sig = self.mapper.create_radioactive_signature_from_topology(state)
        
        metadata = {
            'isotope': sig['isotope'],
            'decay_type': sig['decay_type'],
            'h7_index': state['indice'],
            'h7_pair': state['pareja'],
            'quantum_phase': sig['quantum_phase'],
            'mg_polarity': sig['mg_polarity'],
            'topology_state_index': state_idx,
        }
        
        return metadata
    
    def encrypt(
        self,
        plaintext: bytes,
        password: str,
        associated_data: Optional[bytes] = None
    ) -> EncryptedPacket:
        """
        Encripta datos usando AES-256-GCM con clave derivada cuánticamente.
        
        Args:
            plaintext: Datos a encriptar
            password: Contraseña para derivar clave
            associated_data: Datos adicionales autenticados (AAD)
            
        Returns:
            Paquete encriptado con metadata cuántica
        """
        # Generar salt único
        salt = os.urandom(32)
        
        # Derivar clave de 32 bytes (256 bits)
        key = self.key_derivation.derive_key(
            password,
            salt=salt,
            iterations=self.iterations,
            key_length=32
        )
        
        # Generar nonce
        nonce = self._generate_nonce_from_topology(password)
        
        # Crear encriptador AES-GCM
        aesgcm = AESGCM(key)
        
        # Encriptar
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
        
        # Crear metadata cuántica
        metadata = self._create_quantum_metadata(password, salt)
        
        # Crear paquete
        import base64
        packet = EncryptedPacket(
            ciphertext=base64.b64encode(ciphertext).decode('utf-8'),
            nonce=base64.b64encode(nonce).decode('utf-8'),
            salt=base64.b64encode(salt).decode('utf-8'),
            metadata=metadata,
            timestamp=time.time()
        )
        
        return packet
    
    def decrypt(
        self,
        packet: EncryptedPacket,
        password: str,
        associated_data: Optional[bytes] = None
    ) -> bytes:
        """
        Desencripta un paquete encriptado.
        
        Args:
            packet: Paquete encriptado
            password: Contraseña para derivar clave
            associated_data: Datos adicionales autenticados (AAD)
            
        Returns:
            Datos desencriptados
            
        Raises:
            InvalidTag: Si la contraseña es incorrecta o los datos fueron alterados
        """
        import base64
        
        # Decodificar componentes
        ciphertext = base64.b64decode(packet.ciphertext)
        nonce = base64.b64decode(packet.nonce)
        salt = base64.b64decode(packet.salt)
        
        # Derivar clave usando el mismo salt
        key = self.key_derivation.derive_key(
            password,
            salt=salt,
            iterations=self.iterations,
            key_length=32
        )
        
        # Crear desencriptador AES-GCM
        aesgcm = AESGCM(key)
        
        # Desencriptar
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
            return plaintext
        except InvalidTag:
            raise ValueError("Decryption failed: Invalid password or corrupted data")
    
    def verify_signature(self, packet: EncryptedPacket) -> bool:
        """
        Verifica la integridad de la metadata cuántica.
        
        Args:
            packet: Paquete a verificar
            
        Returns:
            True si la metadata es válida
        """
        metadata = packet.metadata
        
        # Verificar campos requeridos
        required_fields = [
            'isotope', 'decay_type', 'h7_index', 'h7_pair',
            'quantum_phase', 'mg_polarity', 'topology_state_index'
        ]
        
        for field in required_fields:
            if field not in metadata:
                return False
        
        # Verificar conservación H7
        h7_sum = metadata['h7_index'] + metadata['h7_pair']
        if h7_sum != 7:
            return False
        
        # Verificar isótopo válido
        valid_isotopes = ['Sr90', 'Tc99m', 'Pu238']
        if metadata['isotope'] not in valid_isotopes:
            return False
        
        # Verificar índice de estado topológico
        if not (0 <= metadata['topology_state_index'] < 6):
            return False
        
        return True
    
    def encrypt_file(self, input_path: str, output_path: str, password: str):
        """
        Encripta un archivo.
        
        Args:
            input_path: Ruta del archivo a encriptar
            output_path: Ruta del archivo encriptado
            password: Contraseña
        """
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        
        packet = self.encrypt(plaintext, password)
        
        with open(output_path, 'w') as f:
            f.write(packet.to_json())
    
    def decrypt_file(self, input_path: str, output_path: str, password: str):
        """
        Desencripta un archivo.
        
        Args:
            input_path: Ruta del archivo encriptado
            output_path: Ruta del archivo desencriptado
            password: Contraseña
        """
        with open(input_path, 'r') as f:
            packet = EncryptedPacket.from_json(f.read())
        
        plaintext = self.decrypt(packet, password)
        
        with open(output_path, 'wb') as f:
            f.write(plaintext)
