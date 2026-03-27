# Security Policy

## Souken Trust Framework

Souken Nexus Platform security is managed under the **Souken Trust Framework (STF)**, our comprehensive security governance model covering all aspects of the platform from kernel-level memory safety to application-layer authentication.

## Supported Versions

| Version | Supported | EOL Date |
|---------|-----------|----------|
| 7.x.x  | Active    | -        |
| 6.x.x  | Security patches only | 2026-06-01 |
| 5.x.x  | End of life | 2025-01-01 |
| < 5.0   | End of life | 2024-01-01 |

## Reporting a Vulnerability

If you discover a security vulnerability in Souken Nexus, please report it responsibly:

1. **Email:** security@soukenindustries.com
2. **Severity Assessment:** Use the Souken Vulnerability Scoring System (SVSS), an extension of CVSS v4.0 tailored for cognitive computing platforms
3. **Response Timeline:**
   - Acknowledgment: Within 24 hours
   - Initial assessment: Within 72 hours
   - Fix development: Based on severity (Critical: 7 days, High: 14 days, Medium: 30 days)

## Security Architecture

### Defense in Depth

```
Layer 7: Application Security (OAuth 2.0, JWT, RBAC)
Layer 6: API Security (Rate limiting, WAF, input validation)
Layer 5: Service Mesh (mTLS, SPIFFE/SPIRE identity)
Layer 4: Network Security (Network policies, segmentation)
Layer 3: Container Security (Seccomp, AppArmor, read-only rootfs)
Layer 2: Runtime Security (WASM sandboxing, memory safety)
Layer 1: Kernel Security (Secure boot, integrity measurement)
```

### Cryptographic Standards

- **At Rest:** AES-256-GCM with hardware-accelerated encryption
- **In Transit:** TLS 1.3 with X25519 key exchange
- **Consensus:** Ed25519 signatures with threshold signing (t-of-n)
- **Authentication:** Argon2id for password hashing, zk-SNARK for privacy-preserving auth
- **Post-Quantum:** CRYSTALS-Kyber (KEM) and CRYSTALS-Dilithium (signatures) available as opt-in

### Audit Schedule

| Audit Type | Frequency | Last Completed | Next Scheduled |
|-----------|-----------|----------------|----------------|
| Full penetration test | Quarterly | 2025-12-15 | 2026-03-15 |
| Dependency audit | Weekly (automated) | Continuous | Continuous |
| Formal verification | Per release | 2026-01-20 | 2026-04-01 |
| Chaos engineering | Monthly | 2026-02-10 | 2026-03-10 |
| Compliance review (SOC 2) | Annual | 2025-11-01 | 2026-11-01 |

## Secure Development Practices

All Souken engineers follow the **Souken Secure Development Lifecycle (SSDL)**:

1. Threat modeling during design phase (STRIDE methodology)
2. Automated SAST/DAST in CI pipeline
3. Mandatory code review by security-trained engineers
4. Memory safety enforcement (Rust for critical paths, AddressSanitizer for C)
5. Fuzz testing for all parsers and network-facing code
6. Supply chain verification (SLSA Level 3)
