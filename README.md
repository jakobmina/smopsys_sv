<p align="center">
  <img width="128" height="111" alt="logo" src="https://github.com/user-attachments/assets/875e9ac7-6414-44d2-a571-cf385117cff0" />
</p>

# BiMoType-Ternary: The Metriplectic Quantum Framework

> **Bridging Ternary Topology, Nuclear Physics, and Secure P2P Quantum Communication**

![Quantum](https://img.shields.io/badge/Smopsys-Software-black?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Handshake%20Mutuo-8A2BE2?style=for-the-badge)
[![Tests](https://img.shields.io/badge/tests-39%2F39%20passing-brightgreen?style=for-the-badge)](tests/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge)](https://www.python.org/)

BiMoType-Ternary is a high-performance framework that unifies **topological quantum computing** with **nuclear physics signatures**. By leveraging ternary logic (-1, 0, +1) and the rigorous **Metriplectic Mandate**, it provides a stable and physically verifiable substrate for quantum communication and cryptography.

---

## 📜 El Mandato Metriplético (Core Philosophy)

This framework is built upon the foundational principles of Metriplectic dynamics:

1. **Symplectic Component (Hamiltonian $H$)**: Generates conservative, reversible motion (Schrödinger evolution).
2. **Metric Component (Entropy $S$)**: Generates irreversible relaxation toward an attractor (Radioactive decay).
3. **No Singularities**: We balance the dual brackets to avoid numerical explosion or thermal death.
4. **Golden Operator ($O_n$)**: All simulation space is modulated by $O_n = \cos(\pi n) \cdot \cos(\pi \phi n)$, where $\phi \approx 1.618$.

---

## 🚀 Key Features

### 🔐 Multi-Layer Security

- **Metriplectic Cryptography**: Encryption anchored in radioactive decay topology.
- **Hardware Fingerprinting**: Devices are identified by unique hardware-recursive signatures.
- **Mutual Handshake Protocol**: "Deny-by-Default" security. All P2P connections must be explicitly authorized.

### 📡 Secure P2P Networking

- **Decentralized Discovery**: Automatic peer registration and discovery via local cache.
- **Topological Packets**: Data is encoded into ternary BiMoType packets for maximum resilience.
- **Handshake Verification**: Automatic filtering of unauthorized data packets.

### 🧬 Interactive Dashboard

- **Metriplectic Console**: Real-time visualization of P2P activity, identity management, and secure chat.
- **Glassmorphism UI**: High-premium dark theme optimized for technical workflows.

---

## 📦 Installation

```bash
# Recomendado: Entorno virtual
python3 -m venv env
source env/bin/activate

# Instalación directa desde PyPI (Próximamente v1.3.0)
pip install bimotype-ternary

# Instalación modo desarrollo
pip install -e ".[all]"
```

---

## 🛠️ Usage

### Launching the Dashboard (GUI)

The most interactive way to use BiMoType is through the Streamlit-based dashboard:

```bash
python main.py --gui
```

### P2P Communication via CLI

You can also run listening peers or send data via command line:

```bash
# Iniciar escucha P2P
python main.py --listen

# Enviar mensaje a un fingerprint específico
python main.py --send <DEST_FINGERPRINT> --message "HELLO_H7"
```

### Key Generation Demo

```bash
python main.py --crypto 42
```

---

## 🏗️ Project Structure

```text
bimotype-ternary/
├── bimotype_ternary/     # Nucleo de la Librería
│   ├── core/             # 🧠 Session & Recursive Engines
│   ├── crypto/           # 🔐 Criptografía & Handshaking
│   ├── database/         # 🗄️ Persistencia SQLite & Modelos
│   ├── network/          # 📡 P2P, Discovery & Handshake Protocol
│   ├── physics/          # ⚛️ Dinámica Metriplética
│   └── topology/         # 🌀 Codificación Ternaria & H7
├── gui.py                # 🧬 Streamlit Dashboard
├── main.py               # 🚀 Entry Point Unificado
└── tests/                # 🧪 Suite de Pruebas (Seguridad & P2P)
```

---

## 🧪 Verification

Mantenemos un rigor físico y matemático absoluto. Todos los cambios en la capa P2P y Seguridad deben superar los tests de inyección y autorización:

```bash
pytest tests/test_p2p.py
```

---

## 📄 License & Credits

- **Autor**: Jacobo Tlacaelel Mina Rodriguez
- **Principios**: Marco de la Analogía Rigurosa (TLACA)
- **Licencia**: MIT

*Built for a rigorous and secure quantum future.*
