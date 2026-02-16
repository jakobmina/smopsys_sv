# Project Structure

```
bimotype-ternary/
├── bimotype_ternary/          # Main package
│   ├── core/                  # Data structures
│   ├── topology/              # Topology encoding
│   ├── integration/           # BiMoType integration
│   ├── codegen/               # C code generation
│   ├── utils/                 # Utilities
│   └── tests/                 # Test suite (36 tests)
│
├── examples/                  # Usage examples
│   ├── demo.py               # Full demonstration
│   └── quickstart.py         # Quick start guide
│
├── docs/                      # Documentation
│   └── STRUCTURE.md          # Detailed structure
│
├── README.md                  # Main documentation
├── setup.py                   # Package setup
└── requirements.txt           # Dependencies
```

## Installation

```bash
# Install in development mode
pip install -e .

# Or install from PyPI (when published)
pip install bimotype-ternary
```

## Quick Usage

```python
from bimotype_ternary import (
    TernaryBiMoTypeEncoder,
    TernaryBiMoTypeDecoder
)

# Encode
encoder = TernaryBiMoTypeEncoder()
encoded = encoder.encode_message_with_topology("QUANTUM")
packet = encoder.create_bimotype_packet_from_ternary(encoded)

# Decode
decoder = TernaryBiMoTypeDecoder()
decoded = decoder.decode_bimotype_packet(packet, noise_level=0.1)
print(f"Fidelity: {decoded['average_fidelity']:.4f}")
```

## Running Tests

```bash
cd bimotype_ternary/tests
pytest -v
```

See [STRUCTURE.md](docs/STRUCTURE.md) for detailed module documentation.
