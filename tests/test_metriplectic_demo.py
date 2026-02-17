import pytest
import numpy as np
from examples.metriplectic_demo import MetriplecticSystem

def test_metriplectic_rules():
    """Valida el cumplimiento de El Mandato Metriplético"""
    system = MetriplecticSystem("TEST")
    
    # Regla 3.1: Lagrangiano Explícito
    L_symp, L_metr = system.compute_lagrangian()
    assert isinstance(L_symp, (float, np.float64))
    assert isinstance(L_metr, (float, np.float64))
    
    # Regla 1.3: No nulidad (prohibición de singularidades)
    assert abs(L_symp) > 0
    assert abs(L_metr) > 0
    
    # Regla 2.1: Operador Áureo
    n = np.array([1, 2, 3])
    on = system.golden_operator(n)
    assert len(on) == 3
    assert np.all(np.abs(on) <= 1.0)

def test_evolution_convergence():
    """Valida la convergencia del sistema disipativo"""
    system = MetriplecticSystem("ABC")
    initial_psi = system.psi.copy()
    
    system.evolve(steps=10)
    
    # El sistema debe haber cambiado
    assert not np.array_equal(initial_psi, system.psi)
    
    # rho y v deben actualizarse
    assert len(system.rho) == len(system.psi)
    assert len(system.v) == len(system.psi)

def test_nomenclature():
    """Regla 3.2: Nomenclatura Estándar"""
    system = MetriplecticSystem("NOM")
    assert hasattr(system, 'psi')
    assert hasattr(system, 'rho')
    assert hasattr(system, 'v')
