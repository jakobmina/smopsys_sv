<p align="center">
  <img width="128" height="111" alt="logo" src="https://github.com/user-attachments/assets/875e9ac7-6414-44d2-a571-cf385117cff0" />

</p>

# BiMoType-Ternary: The Metriplectic Quantum Framework

> **Bridging Ternary Topology, Nuclear Physics, and Quantum Cryptography**



![Quantum](https://img.shields.io/badge/Smopsys-Software-black)
[![Tests](https://img.shields.io/badge/tests-36%2F36%20passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

BiMoType-Ternary is a high-performance framework that unifies **topological quantum computing** with **nuclear physics signatures**. By leveraging ternary logic (-1, 0, +1) and the rigorous **Metriplectic Mandate**, it provides a stable and physically verifiable substrate for quantum communication and cryptography.

---

## 📜 El Mandato Metriplético (Core Philosophy)

This framework is built upon the foundational principles of Metriplectic dynamics, ensuring that every simulation or theoretical construct is physically robust:

1. **Symplectic Component (Hamiltonian $H$)**: Generates conservative, reversible motion (e.g., Schrödinger evolution, quantum phase advection).
2. **Metric Component (Entropy $S$)**: Generates irreversible relaxation toward an attractor (e.g., radioactive decay, viscosity).
3. **Prohibición de Singularidades**: Purely conservative systems explode; purely dissipative systems die. We balance both.
4. **Golden Operator ($O_n$)**: The vacuum is structured. All space is modulated by $O_n = \cos(\pi n) \cdot \cos(\pi \phi n)$, where $\phi \approx 1.618$.

---

## 📦 Installation

Install the library directly from PyPI:

```bash
pip install bimotype-ternary
```

For development or full features:

```bash
# Clone and install with all extras
git clone https://github.com/jakobmina/smopsys_sv.git
cd smopsys_sv
pip install -e ".[all]"
```

---

## 🚀 Key Modules

### 1. Quantum Cryptography (`.crypto`)

Secure password generation and file encryption anchored in nuclear topology.

* **Entropy**: Mixed from system CSPRNG, topological states, and radioactive signatures.
* **Encryption**: AES-256-GCM with quantum-verified metadata.

```python
from bimotype_ternary.crypto import QuantumPasswordGenerator, QuantumEncryptor

# Generate a quantum-hardened password
gen = QuantumPasswordGenerator()
pwd = gen.generate(length=16, charset='all')

# Encrypt a message with radioactive metadata
enc = QuantumEncryptor()
packet = enc.encrypt(b"Top Secret", password=pwd)
print(f"Signed with: {packet.metadata['isotope']} ({packet.metadata['decay_type']})")
```

### 2. Metriplectic Physics (`.physics`)

Simulates the evolution of systems respecting dual-bracket dynamics.

```python
# See examples/metriplectic_demo.py for a full simulation
# Balance of Symplectic (Conservative) and Metric (Dissipative) terms
lagrangian = system.compute_lagrangian()
params = (lagrangian.L_symp, lagrangian.L_metr)
```

### 3. Ternary Topology (`.topology`)

Encoding information into 3 fundamental states mapped to ALPHA, BETA, and GAMMA decays.

* **Big-Endian Encoding**: High-density packing for embedded smopsys Q-CORE.
* **H7 Conservation**: Invariants satisfying `index + pair = 7`.

---

## 🛠️ Examples & Tools

Explore the `examples/` directory for ready-to-use demonstrations:

* **[crypto_demo.py](examples/crypto_demo.py)**: Full walkthrough of password hardening and file encryption.
* **[metriplectic_demo.py](examples/metriplectic_demo.py)**: Physics simulation of Hamiltonian-Dissipative competition.
* **[demo.py](examples/demo.py)**: High-level BiMoType integration and noise-resilient decoding.

---

## 🏗️ Project Structure

```text
bimotype-ternary/
├── bimotype_ternary/     # Core library
│   ├── crypto/           # 🔐 Quantum encryption & passwords
│   ├── physics/          # ⚛️ Metriplectic dynamics
│   ├── topology/         # 🌀 Ternary & H7 encoding
│   ├── integration/      # 🔗 BiMoType bridge
│   └── codegen/          # 💻 Embedded C generation
├── tests/                # Comprehensive test suite (36 tests)
└── examples/             # Tutorials and CLI demos
```

---

## 🧪 Verification

We maintain 100% test pass rate for all topological and cryptographic logic.

```bash
pytest tests/
```

---

## 📄 License & Credits

* **Author**: Jacobo Tlacaelel Mina Rodriguez
* **Principles**: El Mandato Metriplético
* **License**: MIT

*Built with ❤️ for a rigorous quantum future.*
