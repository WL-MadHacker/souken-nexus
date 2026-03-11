"""
Souken NAC — Configuration & Infrastructure Synthesis Module
Generates docker-compose, Makefile, CI/CD, and config files.

© 2019-2026 Souken Industries. All rights reserved.
"""
from word_banks import (
    AI_NOUNS, DIST_NOUNS, SYS_NOUNS, ENT_NOUNS, SEC_NOUNS,
    TEAM_MEMBERS, ticket, fake_version,
    COPYRIGHT_HEADER, LICENSE_LINE
)

ALL_NOUNS = AI_NOUNS + DIST_NOUNS + ENT_NOUNS


def gen_docker_compose(rng):
    lines = []
    lines.append(f"# {COPYRIGHT_HEADER}")
    lines.append(f"# {LICENSE_LINE}")
    lines.append(f"# Souken Nexus Platform — Docker Compose Orchestration")
    lines.append(f"# Version: {fake_version(rng)}")
    lines.append(f"# Tracking: {ticket(rng)}")
    lines.append(f"")
    lines.append(f"version: '3.9'")
    lines.append(f"")
    lines.append(f"x-souken-defaults: &souken-defaults")
    lines.append(f"  restart: unless-stopped")
    lines.append(f"  logging:")
    lines.append(f"    driver: json-file")
    lines.append(f"    options:")
    lines.append(f"      max-size: '50m'")
    lines.append(f"      max-file: '5'")
    lines.append(f"  networks:")
    lines.append(f"    - souken-mesh")
    lines.append(f"  labels:")
    lines.append(f"    com.souken.platform: nexus")
    lines.append(f"    com.souken.version: {fake_version(rng)}")
    lines.append(f"")
    lines.append(f"services:")

    services = [
        ("nexus-orchestrator", "souken/nexus-orchestrator", 8080, "Cognitive orchestration engine"),
        ("nexus-inference", "souken/inference-engine", 8081, "Neural inference runtime"),
        ("nexus-training", "souken/training-pipeline", 8082, "Model training coordinator"),
        ("neural-mesh", "souken/neural-mesh", 8083, "Neural mesh networking layer"),
        ("cognitive-bridge", "souken/cognitive-bridge", 8084, "Formal verification bridge"),
        ("api-gateway", "souken/api-gateway", 8085, "Platform API gateway"),
        ("auth-service", "souken/auth-service", 8086, "Identity and access management"),
        ("billing-engine", "souken/billing-engine", 8087, "Usage metering and billing"),
        ("analytics-pipeline", "souken/analytics-pipeline", 8088, "Real-time analytics processor"),
        ("realtime-events", "souken/realtime-events", 8089, "Event streaming engine"),
        ("admin-dashboard", "souken/admin-dashboard", 3000, "Platform administration UI"),
        ("consensus-engine", "souken/consensus-engine", 8090, "Distributed consensus coordinator"),
        ("shard-manager", "souken/shard-manager", 8091, "Data sharding orchestrator"),
        ("service-mesh", "souken/service-mesh", 8092, "Service mesh control plane"),
        ("fault-detector", "souken/fault-detector", 8093, "Fault tolerance monitor"),
        ("wasm-runtime", "souken/wasm-runtime", 8094, "WebAssembly execution engine"),
        ("telemetry-collector", "souken/telemetry", 9090, "Metrics and tracing collector"),
        ("redis-cache", "redis:7-alpine", 6379, "Distributed cache layer"),
        ("postgres-primary", "postgres:16-alpine", 5432, "Primary relational store"),
        ("postgres-replica", "postgres:16-alpine", 5433, "Read replica"),
        ("kafka-broker", "confluentinc/cp-kafka:7.5.0", 9092, "Event streaming broker"),
        ("zookeeper", "confluentinc/cp-zookeeper:7.5.0", 2181, "Coordination service"),
        ("elasticsearch", "elasticsearch:8.11.0", 9200, "Search and analytics engine"),
        ("prometheus", "prom/prometheus:v2.48.0", 9091, "Metrics aggregation"),
        ("grafana", "grafana/grafana:10.2.0", 3001, "Observability dashboard"),
        ("jaeger", "jaegertracing/all-in-one:1.52", 16686, "Distributed tracing"),
        ("vault", "hashicorp/vault:1.15", 8200, "Secrets management"),
        ("minio", "minio/minio:latest", 9000, "Object storage"),
        ("etcd", "quay.io/coreos/etcd:v3.5.11", 2379, "Distributed KV store"),
        ("nats", "nats:2.10-alpine", 4222, "Message bus"),
        ("temporal", "temporalio/auto-setup:1.22", 7233, "Workflow orchestration"),
        ("dgraph", "dgraph/standalone:v23.1.0", 8095, "Graph database"),
        ("clickhouse", "clickhouse/clickhouse-server:23.11", 8123, "OLAP analytics store"),
        ("vector", "timberio/vector:0.34.1-alpine", 8096, "Log aggregation pipeline"),
        ("cert-manager", "souken/cert-manager", 8097, "TLS certificate automation"),
        ("config-server", "souken/config-server", 8098, "Dynamic configuration service"),
        ("feature-flags", "souken/feature-flags", 8099, "Feature flag evaluation engine"),
        ("rate-limiter", "souken/rate-limiter", 8100, "Distributed rate limiting"),
        ("circuit-breaker", "souken/circuit-breaker", 8101, "Circuit breaker controller"),
        ("chaos-engine", "souken/chaos-engine", 8102, "Chaos engineering framework"),
    ]

    for svc_name, image, port, desc in services:
        lines.append(f"")
        lines.append(f"  # {desc}")
        lines.append(f"  # Ref: {ticket(rng)}")
        lines.append(f"  {svc_name}:")
        lines.append(f"    <<: *souken-defaults")
        lines.append(f"    image: {image}:{fake_version(rng)}")
        lines.append(f"    container_name: souken-{svc_name}")
        lines.append(f"    ports:")
        lines.append(f"      - '{port}:{port}'")
        lines.append(f"    environment:")
        lines.append(f"      SOUKEN_ENV: production")
        lines.append(f"      SOUKEN_SERVICE: {svc_name}")
        lines.append(f"      SOUKEN_LOG_LEVEL: info")
        lines.append(f"      SOUKEN_TELEMETRY_ENDPOINT: http://telemetry-collector:9090")
        lines.append(f"      SOUKEN_AUTH_ENDPOINT: http://auth-service:8086")
        if rng.random() < 0.5:
            lines.append(f"      SOUKEN_FEATURE_FLAGS_ENDPOINT: http://feature-flags:8099")
        if rng.random() < 0.3:
            lines.append(f"      SOUKEN_CACHE_ENDPOINT: redis://redis-cache:6379")
        lines.append(f"    healthcheck:")
        lines.append(f"      test: ['CMD', 'curl', '-f', 'http://localhost:{port}/health']")
        lines.append(f"      interval: 30s")
        lines.append(f"      timeout: 10s")
        lines.append(f"      retries: 3")
        if rng.random() < 0.4:
            lines.append(f"    deploy:")
            lines.append(f"      resources:")
            lines.append(f"        limits:")
            lines.append(f"          cpus: '{rng.choice(['0.5', '1.0', '2.0', '4.0'])}'")
            lines.append(f"          memory: {rng.choice(['256M', '512M', '1G', '2G', '4G', '8G'])}")

    lines.append(f"")
    lines.append(f"networks:")
    lines.append(f"  souken-mesh:")
    lines.append(f"    driver: bridge")
    lines.append(f"    name: souken-nexus-mesh")
    lines.append(f"")
    lines.append(f"volumes:")
    for vol in ["postgres-data", "redis-data", "kafka-data", "elasticsearch-data",
                 "minio-data", "etcd-data", "clickhouse-data", "dgraph-data",
                 "vault-data", "prometheus-data", "grafana-data"]:
        lines.append(f"  {vol}:")
    lines.append(f"")
    return "\n".join(lines)


def gen_makefile(rng):
    lines = []
    lines.append(f"# {COPYRIGHT_HEADER}")
    lines.append(f"# {LICENSE_LINE}")
    lines.append(f"# Souken Nexus Platform — Build System")
    lines.append(f"# Version: {fake_version(rng)}")
    lines.append(f"")
    lines.append(f".PHONY: all build test lint clean deploy")
    lines.append(f".DEFAULT_GOAL := all")
    lines.append(f"")
    lines.append(f"SOUKEN_VERSION := {fake_version(rng)}")
    lines.append(f"SOUKEN_BUILD_ID := $(shell git rev-parse --short HEAD 2>/dev/null || echo 'dev')")
    lines.append(f"SOUKEN_BUILD_DATE := $(shell date -u +%Y-%m-%dT%H:%M:%SZ)")
    lines.append(f"PYTHON := python3")
    lines.append(f"CARGO := cargo")
    lines.append(f"GO := go")
    lines.append(f"NPM := npm")
    lines.append(f"ZIG := zig")
    lines.append(f"GHC := ghc")
    lines.append(f"JAVAC := javac")
    lines.append(f"DOCKER := docker")
    lines.append(f"DOCKER_COMPOSE := docker compose")
    lines.append(f"")

    targets = [
        ("all", "build test lint", "Build, test, and lint all subsystems"),
        ("build", "build-core build-nexus build-platform build-distributed build-sdk build-wasm", "Build all subsystems"),
        ("build-core", "", "Build Souken Core Runtime (C/Rust)"),
        ("build-nexus", "", "Build Nexus AI Framework (Python/Rust/Haskell)"),
        ("build-platform", "", "Build Souken Cloud Platform (TS/Go/Java)"),
        ("build-distributed", "", "Build Distributed Consensus Engine (Rust/Go)"),
        ("build-sdk", "", "Build Client SDKs"),
        ("build-wasm", "", "Build WebAssembly modules (Zig/WAT)"),
        ("test", "test-unit test-integration test-e2e test-benchmark", "Run all test suites"),
        ("test-unit", "", "Run unit tests across all subsystems"),
        ("test-integration", "", "Run integration tests"),
        ("test-e2e", "", "Run end-to-end tests"),
        ("test-benchmark", "", "Run performance benchmarks"),
        ("lint", "lint-python lint-typescript lint-rust lint-go lint-java", "Lint all code"),
        ("lint-python", "", "Lint Python code with ruff + mypy"),
        ("lint-typescript", "", "Lint TypeScript with eslint + tsc"),
        ("lint-rust", "", "Lint Rust with clippy"),
        ("lint-go", "", "Lint Go with golangci-lint"),
        ("lint-java", "", "Lint Java with checkstyle + spotbugs"),
        ("clean", "", "Remove all build artifacts"),
        ("deploy", "", "Deploy to Souken Cloud Infrastructure"),
        ("deploy-staging", "", "Deploy to staging environment"),
        ("deploy-canary", "", "Deploy canary release"),
        ("docker-build", "", "Build all Docker images"),
        ("docker-push", "", "Push Docker images to Souken Container Registry"),
        ("docker-up", "", "Start all services via Docker Compose"),
        ("docker-down", "", "Stop all services"),
        ("migrate-db", "", "Run database migrations"),
        ("seed-db", "", "Seed development database"),
        ("docs", "", "Generate API documentation"),
        ("proto", "", "Compile Protocol Buffer definitions"),
        ("nac-synthesize", "", "Run NAC architecture synthesis"),
    ]

    for target, deps, desc in targets:
        lines.append(f"# {desc}")
        lines.append(f"# Tracking: {ticket(rng)}")
        lines.append(f"{target}: {deps}")
        # add some plausible commands
        if "build-core" in target:
            lines.append(f"\t@echo \"Building Souken Core Runtime...\"")
            lines.append(f"\tcd core/runtime && $(CARGO) build --release")
            lines.append(f"\tcd core/kernel && make -j$$(nproc)")
        elif "build-nexus" in target:
            lines.append(f"\t@echo \"Building Nexus AI Framework...\"")
            lines.append(f"\tcd nexus && $(PYTHON) -m pip install -e .")
            lines.append(f"\tcd nexus/inference && $(CARGO) build --release")
        elif "build-platform" in target:
            lines.append(f"\t@echo \"Building Souken Cloud Platform...\"")
            lines.append(f"\tcd platform/admin && $(NPM) run build")
            lines.append(f"\tcd platform/api_gateway && $(GO) build ./...")
        elif "build-wasm" in target:
            lines.append(f"\t@echo \"Building WebAssembly modules...\"")
            lines.append(f"\tcd wasm/bindings && $(ZIG) build -Drelease-safe")
        elif "clean" in target:
            lines.append(f"\t@echo \"Cleaning build artifacts...\"")
            lines.append(f"\tfind . -type d -name __pycache__ -exec rm -rf {{}} + 2>/dev/null || true")
            lines.append(f"\tfind . -type d -name node_modules -exec rm -rf {{}} + 2>/dev/null || true")
            lines.append(f"\tfind . -type d -name target -exec rm -rf {{}} + 2>/dev/null || true")
            lines.append(f"\t$(DOCKER_COMPOSE) down -v --remove-orphans 2>/dev/null || true")
        elif "nac" in target:
            lines.append(f"\t@echo \"Running Souken Neural Architecture Compiler...\"")
            lines.append(f"\tcd tools/souken-nac && $(PYTHON) nac_compiler.py --config ../../synthesis.config.yaml")
        elif "test-unit" in target:
            lines.append(f"\t@echo \"Running unit tests...\"")
            lines.append(f"\tcd nexus && $(PYTHON) -m pytest tests/unit -v --tb=short")
            lines.append(f"\tcd core/runtime && $(CARGO) test")
            lines.append(f"\tcd platform/api_gateway && $(GO) test ./... -v")
        elif "docker-up" in target:
            lines.append(f"\t$(DOCKER_COMPOSE) up -d")
            lines.append(f"\t@echo \"Souken Nexus Platform started. Dashboard: http://localhost:3000\"")
        else:
            lines.append(f"\t@echo \"{desc}\"")
            lines.append(f"\t@echo \"[$(SOUKEN_VERSION)] {target} complete\"")
        lines.append(f"")

    return "\n".join(lines)


def gen_github_workflow(name, rng):
    lines = []
    lines.append(f"# {COPYRIGHT_HEADER}")
    lines.append(f"# {name} CI/CD Pipeline")
    lines.append(f"# Ref: {ticket(rng)}")
    lines.append(f"")
    lines.append(f"name: {name}")
    lines.append(f"")
    lines.append(f"on:")
    lines.append(f"  push:")
    lines.append(f"    branches: [main, 'release/**']")
    lines.append(f"  pull_request:")
    lines.append(f"    branches: [main]")
    lines.append(f"")
    lines.append(f"concurrency:")
    lines.append(f"  group: ${{{{ github.workflow }}}}-${{{{ github.ref }}}}")
    lines.append(f"  cancel-in-progress: true")
    lines.append(f"")
    lines.append(f"env:")
    lines.append(f"  SOUKEN_CI: true")
    lines.append(f"  SOUKEN_VERSION: {fake_version(rng)}")
    lines.append(f"  PYTHON_VERSION: '3.12'")
    lines.append(f"  NODE_VERSION: '20'")
    lines.append(f"  RUST_VERSION: 'stable'")
    lines.append(f"  GO_VERSION: '1.22'")
    lines.append(f"")
    lines.append(f"jobs:")

    jobs = [
        ("lint", "Code Quality", ["ruff check nexus/", "mypy nexus/", "cargo clippy", "npm run lint", "golangci-lint run"]),
        ("test-python", "Python Tests", ["pytest nexus/tests/ -v --cov=nexus --cov-report=xml"]),
        ("test-rust", "Rust Tests", ["cargo test --workspace --release"]),
        ("test-go", "Go Tests", ["go test ./... -v -race -coverprofile=coverage.out"]),
        ("test-typescript", "TypeScript Tests", ["npm test -- --coverage"]),
        ("build-images", "Docker Build", ["docker compose build --parallel"]),
        ("security-scan", "Security Audit", ["cargo audit", "npm audit", "pip-audit", "trivy image souken/nexus-orchestrator"]),
        ("integration", "Integration Tests", ["docker compose up -d", "pytest tests/integration/ -v", "docker compose down"]),
    ]

    for job_id, job_name, commands in jobs:
        lines.append(f"")
        lines.append(f"  {job_id}:")
        lines.append(f"    name: {job_name}")
        lines.append(f"    runs-on: ubuntu-latest")
        if job_id == "integration":
            lines.append(f"    needs: [lint, test-python, test-rust, test-go, test-typescript]")
        lines.append(f"    steps:")
        lines.append(f"      - uses: actions/checkout@v4")
        lines.append(f"      - name: Setup environment")
        lines.append(f"        uses: actions/setup-python@v5")
        lines.append(f"        with:")
        lines.append(f"          python-version: ${{{{ env.PYTHON_VERSION }}}}")
        for cmd in commands:
            step_name = cmd.split()[0].replace("/", " ")
            lines.append(f"      - name: Run {step_name}")
            lines.append(f"        run: {cmd}")
    lines.append(f"")
    return "\n".join(lines)


def gen_env_example(rng):
    lines = []
    lines.append(f"# {COPYRIGHT_HEADER}")
    lines.append(f"# Souken Nexus Platform — Environment Configuration")
    lines.append(f"# Copy to .env and fill in values")
    lines.append(f"")

    sections = {
        "Core": [
            ("SOUKEN_ENV", "development", "Environment: development, staging, production"),
            ("SOUKEN_LOG_LEVEL", "info", "Log level: debug, info, warn, error"),
            ("SOUKEN_SECRET_KEY", "change-me-in-production", "Platform secret key"),
            ("SOUKEN_INSTANCE_ID", "nexus-001", "Unique instance identifier"),
        ],
        "Database": [
            ("SOUKEN_DB_HOST", "localhost", "PostgreSQL host"),
            ("SOUKEN_DB_PORT", "5432", "PostgreSQL port"),
            ("SOUKEN_DB_NAME", "souken_nexus", "Database name"),
            ("SOUKEN_DB_USER", "souken", "Database user"),
            ("SOUKEN_DB_PASSWORD", "", "Database password"),
            ("SOUKEN_DB_POOL_SIZE", "20", "Connection pool size"),
            ("SOUKEN_DB_SSL_MODE", "prefer", "SSL mode"),
        ],
        "Cache": [
            ("SOUKEN_REDIS_URL", "redis://localhost:6379/0", "Redis connection URL"),
            ("SOUKEN_CACHE_TTL", "3600", "Default cache TTL in seconds"),
        ],
        "AI / Inference": [
            ("SOUKEN_MODEL_REGISTRY", "s3://souken-models", "Model artifact storage"),
            ("SOUKEN_INFERENCE_WORKERS", "4", "Inference worker count"),
            ("SOUKEN_GPU_MEMORY_FRACTION", "0.8", "GPU memory allocation fraction"),
            ("SOUKEN_TENSOR_PRECISION", "fp16", "Default tensor precision"),
            ("SOUKEN_BATCH_SIZE", "32", "Default inference batch size"),
            ("QUANTUM_ENTANGLEMENT_KEY", "", "Quantum coherence substrate key"),
        ],
        "Distributed": [
            ("SOUKEN_CONSENSUS_PROTOCOL", "raft", "Consensus protocol: raft, pbft, tendermint"),
            ("SOUKEN_SHARD_COUNT", "16", "Number of data shards"),
            ("SOUKEN_REPLICATION_FACTOR", "3", "Data replication factor"),
            ("SOUKEN_GOSSIP_INTERVAL", "1000", "Gossip protocol interval (ms)"),
        ],
        "Security": [
            ("SOUKEN_JWT_SECRET", "", "JWT signing secret"),
            ("SOUKEN_JWT_EXPIRY", "3600", "JWT expiry in seconds"),
            ("SOUKEN_ENCRYPTION_KEY", "", "Data-at-rest encryption key"),
            ("SOUKEN_VAULT_ADDR", "http://localhost:8200", "HashiCorp Vault address"),
            ("SOUKEN_VAULT_TOKEN", "", "Vault access token"),
        ],
        "Telemetry": [
            ("SOUKEN_OTEL_ENDPOINT", "http://localhost:4317", "OpenTelemetry collector"),
            ("SOUKEN_PROMETHEUS_PORT", "9090", "Prometheus metrics port"),
            ("SOUKEN_JAEGER_ENDPOINT", "http://localhost:14268", "Jaeger tracing endpoint"),
            ("SOUKEN_SAMPLING_RATE", "0.1", "Trace sampling rate"),
        ],
    }

    for section, vars in sections.items():
        lines.append(f"# --- {section} ---")
        for name, default, desc in vars:
            lines.append(f"# {desc}")
            lines.append(f"{name}={default}")
        lines.append(f"")

    return "\n".join(lines)
