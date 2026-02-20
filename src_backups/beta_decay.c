/*
 * beta_decay.c - Simulador de decaimiento beta
 * 
 * Implementa transiciones nucleares con emisión fermiónica
 */

#include "beta_decay.h"
#include "nuclear_states.h"
#include "../drivers/bayesian_serial.h"

/* ============================================================
 * DECAIMIENTO BETA
 * ============================================================ */

BetaDecayResult beta_decay_simulate(const char *parent_name) {
    BetaDecayResult result;
    result.occurred = 0;
    result.Q_value_mev = 0.0f;
    result.fermionic_output = 0;
    
    const NuclearIsotope *parent = nuclear_find_isotope(parent_name);
    
    if (!parent) {
        bayesian_serial_write("[Beta Decay] Parent isotope not found\n");
        return result;
    }
    
    bayesian_serial_write("[Beta Decay] Simulating: ");
    bayesian_serial_write(parent->name);
    bayesian_serial_write(" → ");
    
    // Solo T decae a He-3
    if (parent->name[0] == 'T') {
        const NuclearIsotope *daughter = nuclear_find_isotope("He-3");
        
        if (daughter) {
            result.occurred = 1;
            result.Q_value_mev = 0.01857f;
            result.fermionic_output = 0b11;  // e⁻ + ν̄ₑ
            
            bayesian_serial_write(daughter->name);
            bayesian_serial_write(" + e⁻ + ν̄ₑ\n");
            bayesian_serial_write("[Beta Decay] Q = ");
            bayesian_serial_write_float(result.Q_value_mev, 5);
            bayesian_serial_write(" MeV\n");
        }
    } else {
        bayesian_serial_write("STABLE (no decay)\n");
    }
    
    return result;
}

/* ============================================================
 * QUIRALIDAD FERMIÓNICA
 * ============================================================ */

void beta_decay_compute_chirality(uint8_t fermionic_output) {
    bayesian_serial_write("[Chirality] Fermionic output: ");
    bayesian_serial_write_hex(fermionic_output);
    bayesian_serial_write("\n");
    
    // bit 0: electron (e⁻)
    // bit 1: antineutrino (ν̄ₑ)
    
    int has_electron = (fermionic_output & 0b01) != 0;
    int has_antineutrino = (fermionic_output & 0b10) != 0;
    
    bayesian_serial_write("[Chirality] e⁻: ");
    bayesian_serial_write(has_electron ? "YES" : "NO");
    bayesian_serial_write("\n[Chirality] ν̄ₑ: ");
    bayesian_serial_write(has_antineutrino ? "YES" : "NO");
    bayesian_serial_write("\n");
    
    // Quiralidad: 11 = LEFT, 01 = RIGHT, 00 = CENTER
    if (has_electron && has_antineutrino) {
        bayesian_serial_write("[Chirality] Handedness: LEFT-HANDED\n");
    } else if (has_electron && !has_antineutrino) {
        bayesian_serial_write("[Chirality] Handedness: RIGHT-HANDED\n");
    } else {
        bayesian_serial_write("[Chirality] Handedness: CENTER\n");
    }
}
