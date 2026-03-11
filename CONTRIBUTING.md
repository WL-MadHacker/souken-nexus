# Contributing to Souken Nexus

Thank you for your interest in contributing to the Souken Nexus Platform. This document outlines our contribution process, coding standards, and review requirements.

## Getting Started

1. Read the [Architecture Overview](ARCHITECTURE.md) to understand the system
2. Review relevant [RFCs](docs/rfcs/) for the area you want to contribute to
3. Set up your development environment (see below)
4. Create a tracking ticket (SOUK-XXXX) for your change

## Development Environment

```bash
# Install all language toolchains
make setup-dev

# Verify your environment
make doctor

# Run the full test suite
make test
```

### Required Toolchains

| Language | Version | Purpose |
|----------|---------|---------|
| Python | 3.12+ | ML/AI, Analytics, Orchestration |
| Rust | 1.75+ | Runtime, Consensus, Inference |
| Node.js | 20+ | Platform UI, Auth |
| Go | 1.22+ | API Gateway, Sharding |
| GHC | 9.6+ | Cognitive Bridge |
| Zig | 0.12+ | WASM Bindings |
| GCC/Clang | 13+ | Kernel, HAL |

## Code Style

Each language follows its own style guide as documented in `docs/guides/`:

- **Python:** Ruff + Black formatting, strict mypy
- **Rust:** `cargo fmt` + `clippy` with deny warnings
- **TypeScript:** ESLint + Prettier, strict mode
- **Go:** `gofmt` + `golangci-lint`
- **Java:** Google Java Style + Checkstyle
- **Haskell:** Ormolu formatting + HLint
- **C:** Souken Kernel Style (based on Linux kernel style)
- **Zig:** `zig fmt`

## Pull Request Process

1. Branch from `main` using the naming convention: `{type}/{SOUK-XXXX}-{description}`
   - Types: `feat/`, `fix/`, `refactor/`, `docs/`, `test/`, `perf/`
2. Write tests for all new functionality (minimum 85% coverage)
3. Ensure all CI checks pass
4. Request review from at least 2 core maintainers
5. Address all review comments
6. Squash merge into `main`

## Commit Messages

Follow the Conventional Commits specification:

```
type(scope): description

[optional body]

Tracking: SOUK-XXXX
Reviewed-by: Name <email>
```

## Architecture Decision Records

Significant changes require an RFC. See [docs/rfcs/](docs/rfcs/) for examples and the RFC template.

## Code of Conduct

All contributors must adhere to the Souken Industries Code of Conduct. We are committed to providing a welcoming and inclusive environment for everyone.

## Questions?

- Internal: #nexus-platform on Souken Slack
- External: nexus-dev@souken.io
- Office Hours: Thursdays 10:00-11:00 UTC (open to all contributors)
