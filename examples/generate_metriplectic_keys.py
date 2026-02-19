import numpy as np
import matplotlib.pyplot as plt

def aureo_operator(n: int, phi: float = 1.6180339887):
    """Cálculo independiente del operador áureo (Regla 2.1)."""
    n_float = float(n)
    paridad = np.cos(np.pi * n_float)
    fase_mod = np.cos(np.pi * phi * n_float)
    return paridad, fase_mod

class MetriplecticKeyGenerator:
    """
    Genera claves criptográficas basadas en el Mandato Metriplético.
    Cumple con la Regla 1: d_symp (Hamiltoniano) + d_metr (Disipativo).
    """

    def __init__(self, h7_index: int, phi: float = 1.6180339887):
        self.h7_index = h7_index
        self.phi = phi
        self.history = {"symp": [], "metr": []}

    def compute_lagrangian(self, n: int):
        """Regla 3.1: Devuelve componentes por separado."""
        paridad, fase_mod = aureo_operator(n, self.phi)
        
        # Componente Simpléctica (Energía Reversible)
        # modulada por la paridad del operador áureo
        L_symp = np.sin(paridad * self.h7_index)
        
        # Componente Métrica (Disipación / Entropía)
        # modulada por la fase del operador áureo
        L_metr = 0.1 * np.abs(fase_mod) # Factor de disipación pequeño pero presente
        
        return L_symp, L_metr

    def generate_key_sequence(self, length: int = 100):
        """Genera una secuencia de claves modulada por O_n."""
        keys = []
        for n in range(length):
            ls, lm = self.compute_lagrangian(n)
            self.history["symp"].append(ls)
            self.history["metr"].append(lm)
            
            # La clave es la superposición interferencial
            key_val = ls + 1j * lm
            keys.append(key_val)
            
        return np.array(keys)

    def plot_diagnostics(self):
        """Regla 3.3: Visualización de la competencia entre términos."""
        plt.figure(figsize=(12, 6))
        plt.plot(self.history["symp"], label="Comp. Simpléctica (L_symp)", color="cyan", alpha=0.8)
        plt.plot(self.history["metr"], label="Comp. Métrica (L_metr)", color="magenta", alpha=0.8)
        plt.title(f"Diagnóstico Metriplético (H7 Index: {self.h7_index})")
        plt.xlabel("Iteración (n)")
        plt.ylabel("Amplitud")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig("assets/metriplectic_key_diag.png")
        print("📊 Diagnóstico guardado en assets/metriplectic_key_diag.png")

if __name__ == "__main__":
    print("⚛️ Generador de Claves Metriplécticas v1.0")
    print("-" * 40)
    
    # Ejemplo con un índice H7 arbitrario (isótopo hipotético)
    h7_secret = 42 
    generator = MetriplecticKeyGenerator(h7_secret)
    
    print(f"🔑 Generando claves para H7 Index: {h7_secret}...")
    keys = generator.generate_key_sequence(100)
    
    print(f"✅ Secuencia de {len(keys)} claves generada exitosamente.")
    print(f"🔒 Muestra de clave [0]: {keys[0]}")
    
    # Generar visualización diagnóstica (Regla 3.3)
    generator.plot_diagnostics()
