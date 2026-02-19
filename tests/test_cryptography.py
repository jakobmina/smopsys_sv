import pytest
import numpy as np
from examples.generate_metriplectic_keys import MetriplecticKeyGenerator

def test_metriplectic_mandate_rules():
    """Verifica el cumplimiento del Mandato Metriplético."""
    h7_index = 13
    gen = MetriplecticKeyGenerator(h7_index)
    
    ls, lm = gen.compute_lagrangian(1)
    
    # Regla 1.3: Prohibición de singularidades (ni puro symp ni puro metr)
    assert ls != 0, "La componente simpléctica no debe ser cero"
    assert lm != 0, "La componente métrica no debe ser cero"
    
    # Regla 3.1: Método compute_lagrangian explícito
    assert hasattr(gen, "compute_lagrangian"), "Debe tener método compute_lagrangian"

def test_golden_operator_modulation():
    """Verifica que la clave esté modulada por el Operador Áureo."""
    h7_index = 5
    gen = MetriplecticKeyGenerator(h7_index)
    
    keys = gen.generate_key_sequence(10)
    
    # Verificar que no son todas iguales (hay modulación)
    # Se comparan las partes reales
    real_parts = [k.real for k in keys]
    assert len(set(real_parts)) > 1, "La secuencia debe estar modulada por O_n"

def test_key_reproducibility():
    """Verifica que para el mismo H7 e índice n, la clave es idéntica."""
    h7_index = 100
    gen1 = MetriplecticKeyGenerator(h7_index)
    gen2 = MetriplecticKeyGenerator(h7_index)
    
    ls1, lm1 = gen1.compute_lagrangian(5)
    ls2, lm2 = gen2.compute_lagrangian(5)
    
    assert ls1 == ls2
    assert lm1 == lm2
