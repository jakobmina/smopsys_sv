# BiMoType-Ternary Project Structure

```
bimotype-ternary/
│
├── bimotype_ternary/              # Main package
│   ├── __init__.py                # Package exports
│   │
│   ├── core/                      # Core data structures
│   │   ├── __init__.py
│   │   └── datatypes.py           # FirmaRadiactiva, EstadoCuantico, isotopes
│   │
│   ├── topology/                  # Topology encoding
│   │   ├── __init__.py
│   │   └── encoder.py             # Big-endian packing, hex encoding
│   │
│   ├── integration/               # BiMoType integration
│   │   ├── __init__.py
│   │   ├── mapper.py              # Topology ↔ BiMoType mapping
│   │   ├── encoder.py             # Message encoder
│   │   └── decoder.py             # Noise-resilient decoder
│   │
│   ├── codegen/                   # Code generation
│   │   ├── __init__.py
│   │   └── c_generator.py         # C header for Smopsys Q-CORE
│   │
│   ├── utils/                     # Utilities
│   │   ├── __init__.py
│   │   └── psimon_bridge.py       # PSimon integration
│   │
│   └── tests/                     # Test suite
│       ├── test_topology_encoder.py      # 15 tests
│       └── test_bimotype_integration.py  # 21 tests
│
├── examples/                      # Usage examples
│   ├── demo.py                    # Full demo
│   └── quickstart.py              # Quick start
│
├── docs/                          # Documentation
│   └── (future documentation)
│
├── README.md                      # Main documentation
├── setup.py                       # Package setup
└── requirements.txt               # Dependencies
```

## Module Responsibilities

### `core/`

- **datatypes.py**: Core data structures
  - `FirmaRadiactiva`: Radioactive signature
  - `EstadoCuantico`: Quantum state |ψ⟩
  - `TipoDecaimiento`: Decay type enum
  - `RADIOACTIVE_ISOTOPES`: Isotope database

### `topology/`

- **encoder.py**: Topological encoding
  - `CodificadorTopologicoBigEndian`: Big-endian packing
  - `CodificadorHexadecimalBigEndian`: Hex/binary encoding
  - 6 topological states with H7 conservation

### `integration/`

- **mapper.py**: Topology ↔ BiMoType mapping
  - Ternary weight → Decay type
  - H7 index → Quantum phase
  - Chirality → MG polarity

- **encoder.py**: Message encoding
  - `TernaryBiMoTypeEncoder`: Encodes messages
  - Creates BiMoType packets
  - Quantum state generation

- **decoder.py**: Message decoding
  - `TernaryBiMoTypeDecoder`: Decodes packets
  - Noise simulation
  - Fidelity calculation

### `codegen/`

- **c_generator.py**: C code generation
  - `TernaryBiMoTypeCodegen`: Generates C header
  - Smopsys Q-CORE compatible
  - Inline functions for embedded systems

### `utils/`

- **psimon_bridge.py**: PSimon integration
  - Re-exports PSimon components
  - Stub implementation fallback

### `tests/`

- **test_topology_encoder.py**: 15 tests
  - Packing/unpacking
  - Hex encoding
  - H7 conservation

- **test_bimotype_integration.py**: 21 tests
  - Mapping
  - Encoding/decoding
  - Fidelity
  - C header generation

## Import Examples

```python
# Import from top level
from bimotype_ternary import (
    TernaryBiMoTypeEncoder,
    TernaryBiMoTypeDecoder,
    FirmaRadiactiva
)

# Import from submodules
from bimotype_ternary.core import RADIOACTIVE_ISOTOPES
from bimotype_ternary.topology import CodificadorTopologicoBigEndian
from bimotype_ternary.integration import TopologyBiMoTypeMapper
from bimotype_ternary.codegen import TernaryBiMoTypeCodegen
```
