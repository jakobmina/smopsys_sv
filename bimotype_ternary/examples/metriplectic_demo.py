#!/usr/bin/env python3
"""
Metriplectic Usage Example for BiMoType-Ternary.
Fiel al Mandato Metriplético (Core Physics).

Regla 1.1: Componente Simpléctica (Hamiltoniano H).
Regla 1.2: Componente Métrica (Potencial S).
Regla 2.1: Operador Áureo O_n.
Regla 3.2: Nomenclature Standard (psi, rho, v).

Autor: Jacobo Tlacaelel Mina Rodriguez
"""

import numpy as np
import matplotlib.pyplot as plt
from bimotype_ternary import TernaryBiMoTypeEncoder, TernaryBiMoTypeDecoder

class MetriplecticSystem:
    def __init__(self, message: str):
        self.message = message
        self.encoder = TernaryBiMoTypeEncoder()
        self.phi = (1 + np.sqrt(5)) / 2
        
        # Estado inicial (psi: campo cuántico de información)
        self.encoded = self.encoder.encode_message_with_topology(message)
        self.psi = np.array([char['radioactive_signature']['quantum_phase'] for char in self.encoded['encoded_characters']])
        
        # rho: densidad de probabilidad/energía
        self.rho = np.abs(self.psi)**2
        
        # v: flujo de información/velocidad
        self.v = np.gradient(self.psi)
        
        # Historial para visualización
        self.history_h = []
        self.history_s = []

    def golden_operator(self, n: np.ndarray) -> np.ndarray:
        """Regla 2.1: Fondo Estructurado (Operador Áureo O_n)"""
        return np.cos(np.pi * n) * np.cos(np.pi * self.phi * n)

    def compute_lagrangian(self):
        """Regla 1.1, 1.2, 3.1: Lagrangiano Explícito (Symmetric & Metric)"""
        # Hamiltoniano H (Energía de fase) - Componente Simpléctica
        # H = 0.5 * sum(psi^2) * O_n
        n = np.arange(len(self.psi))
        O_n = self.golden_operator(n)
        
        H = 0.5 * np.sum(self.psi**2) * np.mean(O_n)
        L_symp = H
        
        # Potencial de Disipación S (Entropía) - Componente Métrica
        # S = sum(rho * log(rho)) + Viscosidad
        valid_rho = self.rho[self.rho > 0]
        S = -np.sum(valid_rho * np.log(valid_rho)) if len(valid_rho) > 0 else 0
        L_metr = 0.1 * S # Factor de relajación
        
        return L_symp, L_metr

    def evolve(self, steps: int = 100):
        """Simula la evolución metripléctica"""
        print(f"Evolucionando sistema para mensaje: '{self.message}'")
        
        for t in range(steps):
            L_symp, L_metr = self.compute_lagrangian()
            
            self.history_h.append(L_symp)
            self.history_s.append(L_metr)
            
            # Dinámica Simpléctica: dT/dt = {T, H} (simplificado como rotación de fase)
            # Dinámica Métrica: dT/dt = [T, S] (simplificado como amortiguamiento)
            
            # d_symp = Rotación coherente
            d_symp = 0.05 * np.sin(self.psi + t * 0.1)
            
            # d_metr = Decaimiento hacia el atractor (phi)
            d_metr = -0.02 * (self.psi - (1/self.phi))
            
            # Evolución combinada (Regla 1.3: Prohibición de singularidades)
            self.psi += d_symp + d_metr
            self.rho = np.abs(self.psi)**2
            self.v = np.gradient(self.psi)

    def plot_diagnostics(self):
        """Regla 3.3: Visualización Diagnóstica (Conservativo vs Disipativo)"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        steps = range(len(self.history_h))
        
        ax1.plot(steps, self.history_h, label='Hamiltoniano H (Conservativo)', color='blue')
        ax1.plot(steps, self.history_s, label='Potencial S (Disipativo)', color='red')
        ax1.set_title("Competencia Metriplética: H vs S")
        ax1.set_xlabel("Tiempo")
        ax1.set_ylabel("Magnitud")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(range(len(self.psi)), self.psi, marker='o', linestyle='-', color='purple')
        ax2.set_title(f"Canal de Información (psi) para: {self.message}")
        ax2.set_xlabel("Índice de Carácter")
        ax2.set_ylabel("Fase Cuántica (rad)")
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('metriplectic_diagnostics.png')
        print("✓ Diagnóstico guardado en 'metriplectic_diagnostics.png'")

def run_demo():
    system = MetriplecticSystem("BIMOTYPE")
    system.evolve(150)
    system.plot_diagnostics()
    
    # Verificación de decodificación final
    decoder = TernaryBiMoTypeDecoder()
    # Reconstruimos el paquete con el estado evolucionado
    system.encoded['encoded_characters'][0]['radioactive_signature']['quantum_phase'] = system.psi[0]
    
    print("\nResumen Metripléctico:")
    L_s, L_m = system.compute_lagrangian()
    print(f"  L_symp (H): {L_s:.6f}")
    print(f"  L_metr (S): {L_m:.6f}")
    print(f"  Ratio H/S: {L_s/L_m if L_m != 0 else 'inf':.4f}")

if __name__ == "__main__":
    run_demo()
