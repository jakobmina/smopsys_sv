#!/usr/bin/env python3
"""
Tests for Topology Encoder (mod6_mejorado.py)
==============================================

Tests de empaquetamiento/desempaquetamiento topológico
y codificación hexadecimal.

Autor: Jacobo Tlacaelel Mina Rodriguez
"""

import pytest
from bimotype_ternary.topology import (
    CodificadorTopologicoBigEndian,
    CodificadorHexadecimalBigEndian,
    generar_tabla_topologica_completa
)


class TestEmpaquetamientoTopologico:
    """Tests de empaquetamiento/desempaquetamiento"""
    
    def test_empaquetar_estado_1(self):
        """Test empaquetamiento del estado 1"""
        packed = CodificadorTopologicoBigEndian.empaquetar_topologia(
            indice=1,
            pareja=6,
            winding=0,
            mapeo=0,
            peso_ternario=1,
            fase_discreta_fragmento=0
        )
        
        assert packed == 14400  # 0x3840
    
    def test_empaquetar_estado_2(self):
        """Test empaquetamiento del estado 2"""
        packed = CodificadorTopologicoBigEndian.empaquetar_topologia(
            indice=2,
            pareja=5,
            winding=2,
            mapeo=1,
            peso_ternario=-1,
            fase_discreta_fragmento=2
        )
        
        assert packed == 21890  # 0x5582
    
    def test_desempaquetar_estado_1(self):
        """Test desempaquetamiento del estado 1"""
        unpacked = CodificadorTopologicoBigEndian.desempaquetar_topologia(14400)
        
        assert unpacked['indice'] == 1
        assert unpacked['pareja'] == 6
        assert unpacked['winding'] == 0
        assert unpacked['mapeo'] == 0
        assert unpacked['peso_ternario'] == 1
        assert unpacked['fase_discreta_fragmento'] == 0
    
    def test_roundtrip_todos_estados(self):
        """Test roundtrip para todos los estados topológicos"""
        for entry in CodificadorTopologicoBigEndian.topology_entries:
            # Empaquetar
            packed = CodificadorTopologicoBigEndian.empaquetar_topologia(
                entry['indice'],
                entry['pareja'],
                entry['winding'],
                entry['mapeo'],
                entry['peso_ternario'],
                entry['fase_discreta_fragmento']
            )
            
            # Desempaquetar
            unpacked = CodificadorTopologicoBigEndian.desempaquetar_topologia(packed)
            
            # Verificar
            assert unpacked['indice'] == entry['indice']
            assert unpacked['pareja'] == entry['pareja']
            assert unpacked['winding'] == entry['winding']
            assert unpacked['mapeo'] == entry['mapeo']
            assert unpacked['peso_ternario'] == entry['peso_ternario']
            assert unpacked['fase_discreta_fragmento'] == entry['fase_discreta_fragmento']
    
    def test_validacion_indice_fuera_rango(self):
        """Test validación de índice fuera de rango"""
        with pytest.raises(AssertionError):
            CodificadorTopologicoBigEndian.empaquetar_topologia(
                indice=7,  # Fuera de rango
                pareja=1,
                winding=0,
                mapeo=0,
                peso_ternario=0,
                fase_discreta_fragmento=0
            )
    
    def test_validacion_peso_invalido(self):
        """Test validación de peso ternario inválido"""
        with pytest.raises(AssertionError):
            CodificadorTopologicoBigEndian.empaquetar_topologia(
                indice=1,
                pareja=1,
                winding=0,
                mapeo=0,
                peso_ternario=2,  # Inválido (debe ser -1, 0, o 1)
                fase_discreta_fragmento=0
            )


class TestCodificacionHexadecimal:
    """Tests de codificación hexadecimal"""
    
    def test_a_hex_uint16(self):
        """Test conversión a hexadecimal"""
        assert CodificadorHexadecimalBigEndian.a_hex_uint16(14400) == "3840"
        assert CodificadorHexadecimalBigEndian.a_hex_uint16(21890) == "5582"
        assert CodificadorHexadecimalBigEndian.a_hex_uint16(0) == "0000"
        assert CodificadorHexadecimalBigEndian.a_hex_uint16(65535) == "FFFF"
    
    def test_desde_hex_uint16(self):
        """Test conversión desde hexadecimal"""
        assert CodificadorHexadecimalBigEndian.desde_hex_uint16("3840") == 14400
        assert CodificadorHexadecimalBigEndian.desde_hex_uint16("5582") == 21890
        assert CodificadorHexadecimalBigEndian.desde_hex_uint16("0000") == 0
        assert CodificadorHexadecimalBigEndian.desde_hex_uint16("FFFF") == 65535
    
    def test_roundtrip_hex(self):
        """Test roundtrip hexadecimal"""
        for value in [0, 100, 1000, 10000, 32768, 65535]:
            hex_str = CodificadorHexadecimalBigEndian.a_hex_uint16(value)
            recovered = CodificadorHexadecimalBigEndian.desde_hex_uint16(hex_str)
            assert recovered == value
    
    def test_a_binario_uint16(self):
        """Test conversión a binario"""
        assert CodificadorHexadecimalBigEndian.a_binario_uint16(0) == "0000000000000000"
        assert CodificadorHexadecimalBigEndian.a_binario_uint16(1) == "0000000000000001"
        assert CodificadorHexadecimalBigEndian.a_binario_uint16(255) == "0000000011111111"
        assert CodificadorHexadecimalBigEndian.a_binario_uint16(65535) == "1111111111111111"


class TestTablaTopologica:
    """Tests de la tabla topológica completa"""
    
    def test_generar_tabla_completa(self):
        """Test generación de tabla completa"""
        tabla = generar_tabla_topologica_completa()
        
        assert len(tabla) == 6
        
        # Verificar que todos tienen campos requeridos
        for entry in tabla:
            assert 'indice' in entry
            assert 'pareja' in entry
            assert 'peso_ternario' in entry
            assert 'packed_uint16' in entry
            assert 'hex_encoding' in entry
            assert 'binary_encoding' in entry
    
    def test_conservacion_parejas(self):
        """Test conservación de parejas (tipo H7)"""
        # Las parejas deben sumar 7
        for entry in CodificadorTopologicoBigEndian.topology_entries:
            suma = entry['indice'] + entry['pareja']
            assert suma == 7, f"Pareja {entry['indice']}-{entry['pareja']} no suma 7"
    
    def test_distribucion_pesos_ternarios(self):
        """Test distribución de pesos ternarios"""
        pesos = [e['peso_ternario'] for e in CodificadorTopologicoBigEndian.topology_entries]
        
        # Debe haber al menos uno de cada tipo
        assert -1 in pesos
        assert 0 in pesos
        assert 1 in pesos
    
    def test_obtener_estado_topologico(self):
        """Test obtención de estado por índice"""
        estado = CodificadorTopologicoBigEndian.obtener_estado_topologico(0)
        
        assert estado['indice'] == 1
        assert estado['pareja'] == 6
    
    def test_obtener_estado_fuera_rango(self):
        """Test obtención de estado fuera de rango"""
        with pytest.raises(ValueError):
            CodificadorTopologicoBigEndian.obtener_estado_topologico(10)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
