#!/usr/bin/env python3
"""
Bayesian Nuclear Inference - PSimon Integration
================================================

Extiende QuoreMind con lógica bayesiana especializada para estados nucleares.

Combina:
1. BayesLogic (de QuoreMind) → Inferencia general
2. PSimon nuclear states → Estados isotópicos
3. H7 conservation → Prior bayesiano
4. Chiral encoding → Likelihood
5. Beta decay → Transiciones probabilísticas

Autor: Jacobo Tlacaelel Mina Rodriguez
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Importar componentes base
from quoremind_hp import (
        BayesLogic, 
        BayesLogicConfig,
        QuantumBayesMahalanobis
    )
print("[Smopsys] QuoreMind implementation.")
    
class BayesLogicConfig:
      epsilon: float = 1e-6
      high_entropy_threshold: float = 0.8
      high_coherence_threshold: float = 0.6
      action_threshold: float = 0.5
    
@dataclass
class BayesLogic:
    def __init__(self, config=None):
        self.config = config or BayesLogicConfig()
    
    def calculate_posterior_probability(self, prior_a, prior_b, conditional):
        prior_b = max(prior_b, self.config.epsilon)
        return (conditional * prior_a) / prior_b


# Importar PSimon stub (ya definido en psimon_bridge.py)
try:
    from psimon import PSimonStub, IsotopeData
    PSIMON_AVAILABLE = True
except ImportError:
    PSIMON_AVAILABLE = False
    print("[WARNING] PSimon bridge not found. Nuclear inference limited.")


# ============================================================================
# LÓGICA BAYESIANA NUCLEAR
# ============================================================================

class NuclearBayesianInference(BayesLogic):
    """
    Inferencia bayesiana especializada para estados nucleares.
    
    Integra:
    - Prior: Basado en conservación H7
    - Likelihood: Basado en quiralidad y energía de enlace
    - Posterior: Probabilidad de transición nuclear
    """
    
    def __init__(self, config: Optional[BayesLogicConfig] = None):
        super().__init__(config)
        
        # Cache de isótopos
        self.isotopes = PSimonStub.ISOTOPES if PSIMON_AVAILABLE else {}
        
        # Priors aprendidos
        self.learned_priors = {
            'H': 0.15,
            'D': 0.20,
            'T': 0.10,  # Menos probable (radiactivo)
            'He-3': 0.25,
            'He-4': 0.30  # Más probable (más estable)
        }
    
    def calculate_h7_conservation_prior(self, isotope_name: str) -> float:
        """
        Prior basado en conservación H7.
        
        Si h7_index + h7_partner = 7, el prior es alto.
        """
        if not PSIMON_AVAILABLE:
            return 0.5
        
        iso = PSimonStub.get_isotope(isotope_name)
        if not iso:
            return 0.1
        
        # Verificar conservación H7
        h7_sum = iso.h7_index + iso.h7_partner
        
        if h7_sum == 7:
    # H7 conservado: prior alto
            return 0.8
        else:
            # H7 NO conservado: prior bajo
            return 0.2
    
    def calculate_chirality_likelihood(
        self, 
        observed_chirality: float,
        expected_chirality: float
    ) -> float:
        """
        Likelihood basado en quiralidad observada vs esperada.
        
        Usa distribución gaussiana:
        P(observado | esperado) = exp(-0.5 * ((obs - exp) / sigma)^2)
        """
        sigma = 0.3  # Desviación estándar de quiralidad
        
        diff = observed_chirality - expected_chirality
        likelihood = np.exp(-0.5 * (diff / sigma) ** 2)
        
        return float(likelihood)
    
    def calculate_binding_energy_likelihood(
        self,
        observed_mass_u: float,
        isotope_name: str
    ) -> float:
        """
        Likelihood basado en masa observada.
        
        Usa distribución gaussiana centrada en la masa teórica.
        """
        if not PSIMON_AVAILABLE:
            return 0.5
        
        iso = PSimonStub.get_isotope(isotope_name)
        if not iso:
            return 0.1
        
        # Sigma basado en precisión experimental (~0.001 u)
        sigma = 0.001
        
        diff = observed_mass_u - iso.mass_u
        likelihood = np.exp(-0.5 * (diff / sigma) ** 2)
        
        return float(likelihood)
    
    def infer_isotope_from_mass(
        self,
        observed_mass_u: float,
        include_binding_energy: bool = False,
        observed_binding_mev: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Infiere qué isótopo es, dada una masa observada.
        
        Retorna diccionario con probabilidades posteriores para cada isótopo.
        """
        if not PSIMON_AVAILABLE:
            return {'unknown': 1.0}
        
        posteriors = {}
        
        for name, iso in self.isotopes.items():
            # Prior (aprendido)
            prior = self.learned_priors[name]
            
            # Likelihood de masa
            mass_likelihood = self.calculate_binding_energy_likelihood(
                observed_mass_u, name
            )
            
            # Si también tenemos binding energy, usarlo
            if include_binding_energy and observed_binding_mev is not None:
                # Likelihood de energía de enlace
                sigma_energy = 0.1  # MeV
                diff_energy = observed_binding_mev - iso.binding_energy_mev
                energy_likelihood = np.exp(-0.5 * (diff_energy / sigma_energy) ** 2)
                
                # Combinar likelihoods
                likelihood = mass_likelihood * energy_likelihood
            else:
                likelihood = mass_likelihood
            
            # Posterior (sin normalizar)
            posterior_unnorm = prior * likelihood
            posteriors[name] = posterior_unnorm
        
        # Normalizar
        total = sum(posteriors.values())
        if total > 0:
            posteriors = {k: v/total for k, v in posteriors.items()}
        
        return posteriors
    
    def calculate_decay_probability(
        self,
        parent_name: str,
        daughter_name: str,
        time_seconds: float
    ) -> float:
        """
        Calcula probabilidad de decaimiento en tiempo dado.
        
        Para T → He-3:
        P(decay) = 1 - exp(-λ * t)
        
        donde λ = ln(2) / t_1/2
        """
        if parent_name == 'T' and daughter_name == 'He-3':
            # Vida media del tritio: 12.32 años = 3.885e8 segundos
            half_life_seconds = 12.32 * 365.25 * 24 * 3600
            lambda_decay = np.log(2) / half_life_seconds
            
            # Probabilidad de decaimiento
            prob = 1.0 - np.exp(-lambda_decay * time_seconds)
            
            return float(prob)
        
        # Otros isótopos: estables (prob = 0)
        return 0.0
    
    def bayesian_nuclear_decision(
        self,
        observed_state: Dict,
        target_isotope: str,
        action: str = 'identify'
    ) -> Dict:
        """
        Toma de decisión bayesiana para estados nucleares.
        
        Args:
            observed_state: {'mass_u': float, 'binding_mev': float, 'chirality': float}
            target_isotope: Isótopo que queremos identificar/verificar
            action: 'identify', 'verify', 'predict_decay'
        
        Returns:
            Diccionario con decisión y probabilidades
        """
        result = {
            'action': action,
            'target_isotope': target_isotope,
            'decision': None,
            'confidence': 0.0,
            'posteriors': {},
            'reasoning': []
        }
        
        if action == 'identify':
            # Identificar isótopo desde masa
            posteriors = self.infer_isotope_from_mass(
                observed_state.get('mass_u', 0.0),
                include_binding_energy=True,
                observed_binding_mev=observed_state.get('binding_mev')
            )
            
            result['posteriors'] = posteriors
            
            # Decisión: isótopo con mayor posterior
            if posteriors:
                best_isotope = max(posteriors, key=posteriors.get)
                result['decision'] = best_isotope
                result['confidence'] = posteriors[best_isotope]
                result['reasoning'].append(
                    f"Identified as {best_isotope} with {result['confidence']:.2%} confidence"
                )
        
        elif action == 'verify':
            # Verificar si el estado observado corresponde al target
            iso = PSimonStub.get_isotope(target_isotope) if PSIMON_AVAILABLE else None
            
            if iso:
                # Prior de H7
                h7_prior = self.calculate_h7_conservation_prior(target_isotope)
                
                # Likelihood de masa
                mass_likelihood = self.calculate_binding_energy_likelihood(
                    observed_state.get('mass_u', 0.0),
                    target_isotope
                )
                
                # Likelihood de quiralidad
                chirality_likelihood = self.calculate_chirality_likelihood(
                    observed_state.get('chirality', 0.0),
                    iso.chirality_index
                )
                
                # Posterior
                likelihood_combined = mass_likelihood * chirality_likelihood
                posterior = self.calculate_posterior_probability(
                    h7_prior,
                    0.5,  # prior del dato
                    likelihood_combined
                )
                
                result['confidence'] = posterior
                result['decision'] = 'MATCH' if posterior > 0.7 else 'NO_MATCH'
                result['reasoning'].append(
                    f"H7 prior: {h7_prior:.3f}, "
                    f"Mass likelihood: {mass_likelihood:.3f}, "
                    f"Chirality likelihood: {chirality_likelihood:.3f}"
                )
        
        elif action == 'predict_decay':
            # Predecir si habrá decaimiento
            time_s = observed_state.get('time_seconds', 1.0)
            
            # Probabilidad de decaimiento
            decay_prob = self.calculate_decay_probability(
                target_isotope,
                'He-3',  # Asumimos T → He-3
                time_s
            )
            
            result['confidence'] = decay_prob
            result['decision'] = 'DECAY' if decay_prob > 0.5 else 'STABLE'
            result['reasoning'].append(
                f"Decay probability in {time_s}s: {decay_prob:.6f}"
            )
        
        return result


# ============================================================================
# CORRECCIÓN DE ERRORES NUCLEARES (QUANTUM ERROR CORRECTION)
# ============================================================================

class NuclearErrorCorrection(NuclearBayesianInference):
    """
    Corrección de errores en strings binarios nucleares.
    
    Usa inferencia bayesiana para:
    1. Detectar bits corruptos
    2. Calcular probabilidad de corrección
    3. Sugerir correcciones
    """
    
    def calculate_error_probability(
        self,
        observed_binary: str,
        expected_binary: str
    ) -> Tuple[float, List[int]]:
        """
        Calcula probabilidad de error y posiciones corruptas.
        
        Returns:
            (error_rate, corrupted_positions)
        """
        if len(observed_binary) != len(expected_binary):
            return 1.0, []
        
        corrupted_positions = []
        
        for i, (obs_bit, exp_bit) in enumerate(zip(observed_binary, expected_binary)):
            if obs_bit != exp_bit:
                corrupted_positions.append(i)
        
        error_rate = len(corrupted_positions) / len(expected_binary)
        
        return error_rate, corrupted_positions
    
    def correct_nuclear_binary(
        self,
        observed_binary: str,
        isotope_hint: Optional[str] = None
    ) -> Dict:
        """
        Intenta corregir un string binario corrupto.
        
        Args:
            observed_binary: String binario observado (posiblemente corrupto)
            isotope_hint: Pista sobre qué isótopo debería ser
        
        Returns:
            Diccionario con corrección y confianza
        """
        result = {
            'original': observed_binary,
            'corrected': None,
            'confidence': 0.0,
            'errors_detected': 0,
            'error_positions': [],
            'suggestion': None
        }
        
        if not PSIMON_AVAILABLE:
            return result
        
        # Si tenemos hint, comparar directamente
        if isotope_hint:
            iso = PSimonStub.get_isotope(isotope_hint)
            if iso:
                expected_binary = iso.binary_string.replace('_', '')
                
                error_rate, corrupted_pos = self.calculate_error_probability(
                    observed_binary.replace('_', ''),
                    expected_binary
                )
                
                result['errors_detected'] = len(corrupted_pos)
                result['error_positions'] = corrupted_pos
                result['corrected'] = expected_binary
                
                # Confianza: inversamente proporcional al error rate
                result['confidence'] = 1.0 - error_rate
                
                if error_rate < 0.3:
                    result['suggestion'] = 'AUTO_CORRECT'
                elif error_rate < 0.5:
                    result['suggestion'] = 'VERIFY_MANUAL'
                else:
                    result['suggestion'] = 'TOO_CORRUPT'
        
        else:
            # Sin hint: probar todos los isótopos
            best_match = None
            best_error_rate = 1.0
            
            for name, iso in self.isotopes.items():
                expected = iso.binary_string.replace('_', '')
                
                # Padding si es necesario
                if len(observed_binary) != len(expected):
                    continue
                
                error_rate, _ = self.calculate_error_probability(
                    observed_binary.replace('_', ''),
                    expected
                )
                
                if error_rate < best_error_rate:
                    best_error_rate = error_rate
                    best_match = iso
            
            if best_match:
                result['corrected'] = best_match.binary_string
                result['confidence'] = 1.0 - best_error_rate
                result['suggestion'] = f"Likely {best_match.name}"
        
        return result


# ============================================================================
# GENERADOR DE CÓDIGO C
# ============================================================================

class BayesianNuclearCodegen:
    """Genera código C para inferencia bayesiana nuclear en Smopsys"""
    
    @staticmethod
    def generate_header() -> str:
        """Genera bayesian_nuclear.h"""
        
        code = """/*
 * bayesian_nuclear.h - Inferencia Bayesiana Nuclear
 * Smopsys Q-CORE + PSimon Integration
 * 
 * AUTO-GENERATED from quoremind.py + psimon
 */

#ifndef BAYESIAN_NUCLEAR_H
#define BAYESIAN_NUCLEAR_H

#include <stdint.h>
#include "nuclear_states.h"

/* ============================================================
 * ESTRUCTURAS DE DECISIÓN BAYESIANA
 * ============================================================ */

typedef enum {
    NUCLEAR_ACTION_IDENTIFY,
    NUCLEAR_ACTION_VERIFY,
    NUCLEAR_ACTION_PREDICT_DECAY
} NuclearAction;

typedef struct {
    NuclearAction action;
    const char *target_isotope;
    const char *decision;
    float confidence;
    const char *reasoning;
} NuclearBayesianDecision;

/* ============================================================
 * PRIORS APRENDIDOS
 * ============================================================ */

static const float NUCLEAR_LEARNED_PRIORS[] = {
    0.15f,  // H
    0.20f,  // D
    0.10f,  // T (menos probable - radiactivo)
    0.25f,  // He-3
    0.30f   // He-4 (más probable - más estable)
};

/* ============================================================
 * FUNCIONES DE INFERENCIA
 * ============================================================ */

/**
 * Prior basado en conservación H7
 */
static inline float nuclear_h7_conservation_prior(const NuclearIsotope *iso) {
    if (!iso) return 0.1f;
    
    uint8_t h7_sum = iso->h7_index + iso->h7_partner;
    
    return (h7_sum == 7) ? 0.8f : 0.2f;
}

/**
 * Likelihood basado en quiralidad
 */
static inline float nuclear_chirality_likelihood(
    float observed_chirality,
    float expected_chirality
) {
    float sigma = 0.3f;
    float diff = observed_chirality - expected_chirality;
    
    // Gaussiana: exp(-0.5 * (diff/sigma)^2)
    return expf(-0.5f * (diff / sigma) * (diff / sigma));
}

/**
 * Likelihood basado en masa
 */
static inline float nuclear_mass_likelihood(
    float observed_mass_u,
    float expected_mass_u
) {
    float sigma = 0.001f;  // Precisión experimental
    float diff = observed_mass_u - expected_mass_u;
    
    return expf(-0.5f * (diff / sigma) * (diff / sigma));
}

/**
 * Posterior bayesiano
 */
static inline float nuclear_posterior_probability(
    float prior,
    float likelihood,
    float evidence
) {
    if (evidence < 1e-6f) evidence = 1e-6f;
    return (likelihood * prior) / evidence;
}

/**
 * Infiere isótopo desde masa observada
 */
NuclearBayesianDecision nuclear_infer_from_mass(float observed_mass_u);

/**
 * Verifica si estado observado corresponde a target
 */
NuclearBayesianDecision nuclear_verify_isotope(
    const char *target_isotope,
    float observed_mass_u,
    float observed_chirality
);

/**
 * Predice probabilidad de decaimiento
 */
NuclearBayesianDecision nuclear_predict_decay(
    const char *parent_isotope,
    float time_seconds
);

/**
 * Probabilidad de decaimiento T → He-3
 */
static inline float nuclear_tritium_decay_probability(float time_seconds) {
    // Vida media del tritio: 12.32 años
    float half_life_s = 12.32f * 365.25f * 24.0f * 3600.0f;
    float lambda = 0.693147f / half_life_s;  // ln(2) / t_1/2
    
    // P(decay) = 1 - exp(-λt)
    return 1.0f - expf(-lambda * time_seconds);
}

#endif /* BAYESIAN_NUCLEAR_H */
"""
        
        return code


# ============================================================================
# DEMO
# ============================================================================

def demo_bayesian_nuclear():
    """Demuestra inferencia bayesiana nuclear"""
    
    print("=" * 80)
    print("  BAYESIAN NUCLEAR INFERENCE - PSIMON INTEGRATION")
    print("=" * 80)
    
    # Crear inferencia
    bayes = NuclearBayesianInference()
    
    # Demo 1: Identificar isótopo desde masa
    print("\n1. IDENTIFY ISOTOPE FROM MASS")
    print("-" * 80)
    
    test_cases = [
        (2.01410, "Deuterium"),
        (3.01605, "Tritium"),
        (4.00260, "Helium-4")
    ]
    
    for mass, name in test_cases:
        posteriors = bayes.infer_isotope_from_mass(mass)
        
        print(f"\nObserved mass: {mass} u ({name})")
        print("Posteriors:")
        for iso, prob in sorted(posteriors.items(), key=lambda x: -x[1])[:3]:
            print(f"  {iso}: {prob:.4f} ({prob*100:.1f}%)")
    
    # Demo 2: Verificar isótopo
    print("\n\n2. VERIFY ISOTOPE")
    print("-" * 80)
    
    decision = bayes.bayesian_nuclear_decision(
        observed_state={
            'mass_u': 3.01605,
            'binding_mev': 2.827,
            'chirality': 1.0
        },
        target_isotope='T',
        action='verify'
    )
    
    print(f"\nTarget: T (Tritium)")
    print(f"Decision: {decision['decision']}")
    print(f"Confidence: {decision['confidence']:.4f}")
    print(f"Reasoning: {decision['reasoning'],[]}")
    
    # Demo 3: Predecir decaimiento
    print("\n3. PREDICT BETA DECAY")
    print("-" * 80)
    
    times = [1, 3600, 86400, 365.25*86400]  # 1s, 1h, 1d, 1y
    
    for time_s in times:
        decision = bayes.bayesian_nuclear_decision(
            observed_state={'time_seconds': time_s},
            target_isotope='T',
            action='predict_decay'
        )
        
        if time_s < 3600:
            time_str = f"{time_s}s"
        elif time_s < 86400:
            time_str = f"{time_s/3600:.1f}h"
        elif time_s < 365.25*86400:
            time_str = f"{time_s/86400:.1f}d"
        else:
            time_str = f"{time_s/(365.25*86400):.1f}y"
        
        print(f"\nTime: {time_str}")
        print(f"Decay probability: {decision['confidence']:.6e}")
        print(f"Decision: {decision['decision']}")
    
    # Demo 4: Corrección de errores
    print("\n\n4. QUANTUM ERROR CORRECTION")
    print("-" * 80)
    
    error_corrector = NuclearErrorCorrection()
    
    # String corrupto para deuterio (debería ser "01")
    result = error_corrector.correct_nuclear_binary(
        observed_binary="11",  # Corrupto
        isotope_hint="D"
    )
    
    print(f"\nOriginal (corrupted): {result['original']}")
    print(f"Expected (D):         01")
    print(f"Errors detected:      {result['errors_detected']}")
    print(f"Error positions:      {result['error_positions']}")
    print(f"Confidence:           {result['confidence']:.2%}")
    print(f"Suggestion:           {result['suggestion']}")
    
    # Demo 5: Generar código C
    print("\n\n5. GENERATE C CODE")
    print("-" * 80)
    
    codegen = BayesianNuclearCodegen()
    header = codegen.generate_header()
    
    with open('bayesian_nuclear.h', 'w') as f:
        f.write(header)
    
    print("\n✓ Generated: bayesian_nuclear.h")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    demo_bayesian_nuclear()
