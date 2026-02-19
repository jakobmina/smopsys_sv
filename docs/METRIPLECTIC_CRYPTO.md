# Manual de Criptografía Metriplética y Generación de Claves

Este documento describe los principios y procedimientos para la generación de claves criptográficas y la implementación de protocolos de seguridad basados en el **Mandato Metriplético**.

## 1. Fundamentos Físico-Criptográficos

Siguiendo el Mandato, la seguridad no reside solo en la aleatoriedad, sino en la competencia entre dos dinámicas fundamentales:

### 1.1 El Corchete de Criptografía

Cualquier clave o estado cifrado debe definirse mediante la estructura:
$$\frac{d\Psi}{dt} = \{\Psi, H\} + [\Psi, S]$$

* **Componente Simpléctica ($\{\Psi, H\}$):** Representa la permutación reversible del espacio de estados (energía del cifrado). Genera la confusión y difusión clásica.
* **Componente Métrica ($[\Psi, S]$):** Representa la relajación hacia un atractor o la disipación de información ruidosa (entropía). Garantiza que el sistema no explote numéricamente y define la decoherencia del secreto.

> [!IMPORTANT]
> **Prohibición de Singularidades:** No se permiten claves puramente deterministas (vulnerables a criptoanálisis lineal) ni claves puramente aleatorias (ruido térmico sin estructura).

## 2. Generación de Claves (H7-Isotope Mapping)

Las claves se derivan de la estructura nuclear de los isótopos de la Tabla H7.

### 2.1 El Secreto del Oráculo

Se utiliza el **Algoritmo de Simon** para identificar periodos ocultos $s$ en el espacio de estados de los isótopos.

1. **Selección de Isótopo:** Se elige un isótopo base (e.g., $^{229}Th$).
2. **Extracción de Índice H7:** El índice `h7_index` actúa como la semilla del secreto.
3. **Operador Áureo ($O_n$):** La fase de la clave se modula por $O_n = \cos(\pi n) \cdot \cos(\pi \phi n)$, evitando patrones periódicos simples que los atacantes cuánticos podrían explotar.

### 2.2 Estructura de la Clave

Una "Clave Metriplética" es una tupla:
$$K = (H_{key}, S_{key}, \Phi_{aurea})$$

* $H_{key}$: Hamiltoniano de rotación (confusión).
* $S_{key}$: Potencial de disipación (estabilización).
* $\Phi_{aurea}$: Fase de Berry modulada por $\phi$.

## 3. Implementación en Código

Para generar una clave, el sistema debe implementar el método `compute_lagrangian()` que valide la separación de componentes:

```python
def compute_lagrangian(self):
    L_symp = self.calculate_hamiltonian_energy()
    L_metr = self.calculate_dissipative_potential()
    return L_symp, L_metr
```

## 4. Oráculo de Simon y Verificación

El oráculo en C (`simon_oracle.c`) permite verificar la integridad de la clave mediante consultas cuánticas:

1. Se inicializa el oráculo con el `h7_index`.
2. Se ejecutan queries $f(x) = f(x \oplus s)$.
3. La recuperación exitosa de $s$ valida la coherencia de la clave.
