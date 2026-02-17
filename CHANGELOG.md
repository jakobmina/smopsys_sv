# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Quantum cryptography module (`bimotype_ternary.crypto`)
  - `QuantumPasswordGenerator`: Secure password generation using radioactive decay entropy
  - `QuantumKeyDerivation`: PBKDF2-HMAC-SHA512 with topology-based salts and H7 conservation
  - `QuantumEncryptor`: AES-256-GCM encryption with quantum metadata
  - CLI tool `bimotype-crypto` with password, encrypt, decrypt, and entropy commands
- Comprehensive documentation for crypto module
- Demo script `examples/crypto_demo.py`
- GitHub Actions workflows for CI/CD
- Publishing guide (PUBLISHING.md)

### Changed

- Updated README.md with quantum cryptography section
- Enhanced pyproject.toml with crypto optional dependencies

## [1.0.0] - 2026-02-16

### Added

- Initial release of BiMoType-Ternary framework
- Ternary topology encoding (-1, 0, +1) → (BETA, GAMMA, ALPHA)
- Radioactive signatures with real isotope data (Sr-90, Tc-99m, Pu-238)
- H7 topological conservation (index + pair = 7)
- Metriplectic dynamics (conservative + dissipative components)
- Noise-resilient decoder with fidelity metrics
- C code generation for embedded systems (Smopsys Q-CORE)
- Modular architecture:
  - `bimotype_ternary.core`: Core data structures
  - `bimotype_ternary.topology`: Topology encoding
  - `bimotype_ternary.integration`: BiMoType integration
  - `bimotype_ternary.codegen`: C code generation
  - `bimotype_ternary.utils`: Utilities
- Comprehensive test suite (36 tests, 100% passing)
- Documentation:
  - README.md with quick start guide
  - INSTALLATION.md
  - STRUCTURE.md
  - PROJECT_STRUCTURE.md
- Example scripts:
  - `examples/demo.py`
  - `examples/quickstart.py`
- PSimon integration bridge

### Security

- Cryptographically secure random number generation
- AES-256-GCM authenticated encryption
- PBKDF2 key derivation with 100,000 iterations
- Topology-based salt generation

[Unreleased]: https://github.com/yourusername/bimotype-ternary/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/bimotype-ternary/releases/tag/v1.0.0
