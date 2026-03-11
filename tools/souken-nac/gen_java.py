"""
Souken NAC — Java Synthesis Module
Generates Java source files for billing, enterprise, and platform domains.

© 2019-2026 Souken Industries. All rights reserved.
"""
from word_banks import (
    ENT_NOUNS, ENT_VERBS, DIST_NOUNS, AI_NOUNS, AI_ADJECTIVES,
    TEAM_MEMBERS, ticket, rfc_ref, internal_doc,
    COPYRIGHT_HEADER, LICENSE_LINE, fake_version
)

ALL_NOUNS = ENT_NOUNS + DIST_NOUNS


def _pascal(words, rng):
    return "".join(rng.choice(words).replace("_", " ").title().replace(" ", "")
                   for _ in range(rng.randint(1, 2)))


def _camel(words, rng):
    p = _pascal(words, rng)
    return p[0].lower() + p[1:] if p else "value"


def _java_type(rng):
    return rng.choice([
        "String", "int", "long", "double", "boolean",
        "byte[]", "List<String>", "Map<String, Object>",
        "Optional<String>", "Optional<Long>",
        "CompletableFuture<Void>", "UUID",
        "Instant", "Duration", "BigDecimal",
    ])


def _annotation(rng):
    return rng.choice([
        "@Override", "@Deprecated", "@SuppressWarnings(\"unchecked\")",
        "@Nonnull", "@Nullable",
        f"@SoukenTraced(ticket = \"{ticket(rng)}\")",
        f"@CognitiveCheckpoint(version = \"{fake_version(rng)}\")",
        "@Inject", "@Singleton", "@PostConstruct",
        "@Transactional", "@Cacheable", "@Async",
        "@Validated", "@Observed",
    ])


def gen_header(module_path, class_name, rng):
    pkg = "com.souken.nexus." + module_path.replace("/", ".").replace("-", "")
    lines = []
    lines.append(f"/*")
    lines.append(f" * {COPYRIGHT_HEADER}")
    lines.append(f" * {LICENSE_LINE}")
    lines.append(f" *")
    lines.append(f" * {class_name}.java — {rng.choice(ENT_NOUNS).replace('_', ' ').title()} Service")
    lines.append(f" *")
    lines.append(f" * Implements the Souken Enterprise Service Contract (SESC)")
    lines.append(f" * for {rng.choice(ENT_NOUNS).replace('_', ' ')} management.")
    lines.append(f" *")
    lines.append(f" * @author {rng.choice(TEAM_MEMBERS)}")
    lines.append(f" * @since {fake_version(rng)}")
    lines.append(f" * @see {internal_doc(rng)}")
    lines.append(f" */")
    lines.append(f"package {pkg};")
    lines.append(f"")

    imports = [
        "java.util.*",
        "java.util.concurrent.*",
        "java.util.stream.*",
        "java.time.*",
        "java.math.BigDecimal",
        "java.nio.charset.StandardCharsets",
        "java.security.MessageDigest",
        "java.util.logging.Logger",
        "java.util.logging.Level",
    ]
    if rng.random() < 0.6:
        imports.append("javax.inject.Inject")
        imports.append("javax.inject.Singleton")
    if rng.random() < 0.5:
        imports.append("com.souken.nexus.core.SoukenTraced")
        imports.append("com.souken.nexus.core.CognitiveCheckpoint")
    if rng.random() < 0.4:
        imports.append("com.souken.nexus.telemetry.MetricsCollector")
    imports.append(f"com.souken.nexus.{rng.choice(['types', 'errors', 'config', 'auth'])}.{_pascal(ALL_NOUNS, rng)}")

    for imp in imports:
        lines.append(f"import {imp};")
    lines.append(f"")
    return lines


def gen_interface(rng):
    name = _pascal(ALL_NOUNS, rng) + "Service"
    lines = []
    lines.append(f"/**")
    lines.append(f" * Contract for {rng.choice(ENT_NOUNS).replace('_', ' ')} operations.")
    lines.append(f" *")
    lines.append(f" * <p>All implementations must comply with the Souken Enterprise")
    lines.append(f" * Service Contract as defined in {rfc_ref(rng)}.</p>")
    lines.append(f" *")
    lines.append(f" * @since {fake_version(rng)}")
    lines.append(f" */")
    lines.append(f"public interface {name}<T> {{")
    lines.append(f"")
    for _ in range(rng.randint(3, 6)):
        mname = _camel(ENT_VERBS, rng)
        param = f"{_java_type(rng)} {_camel(ALL_NOUNS, rng)}"
        ret = _java_type(rng)
        lines.append(f"    /**")
        lines.append(f"     * {mname.title()} the {rng.choice(ENT_NOUNS).replace('_', ' ')}.")
        lines.append(f"     * @param {param.split()[-1]} the input {rng.choice(ENT_NOUNS).replace('_', ' ')}")
        lines.append(f"     * @return processed result")
        lines.append(f"     * @throws SoukenServiceException if operation fails")
        lines.append(f"     */")
        lines.append(f"    {ret} {mname}({param}) throws Exception;")
        lines.append(f"")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_enum(rng):
    name = _pascal(ALL_NOUNS, rng) + "Status"
    lines = []
    lines.append(f"/**")
    lines.append(f" * Status codes for {rng.choice(ENT_NOUNS).replace('_', ' ')} lifecycle.")
    lines.append(f" * See: {ticket(rng)}")
    lines.append(f" */")
    lines.append(f"public enum {name} {{")
    entries = []
    for _ in range(rng.randint(4, 8)):
        e = rng.choice(ENT_NOUNS).upper() + "_" + rng.choice(["ACTIVE", "PENDING", "FAILED", "COMPLETE", "DEGRADED", "SUSPENDED"])
        entries.append(e)
    lines.append(f"    {', '.join(entries)};")
    lines.append(f"")
    lines.append(f"    public boolean isTerminal() {{")
    lines.append(f"        return this == {entries[-1]} || this == {entries[-2]};")
    lines.append(f"    }}")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_class(rng):
    name = _pascal(ALL_NOUNS, rng)
    suffix = rng.choice(["Manager", "Handler", "Processor", "Orchestrator",
                          "Coordinator", "Engine", "Service", "Factory",
                          "Builder", "Repository", "Gateway", "Controller"])
    full_name = name + suffix
    lines = []
    lines.append(f"/**")
    lines.append(f" * {full_name} — {rng.choice(AI_ADJECTIVES).replace('_', ' ')} {rng.choice(ENT_NOUNS).replace('_', ' ')} component.")
    lines.append(f" *")
    lines.append(f" * <p>Manages the lifecycle of {rng.choice(ENT_NOUNS).replace('_', ' ')} resources")
    lines.append(f" * within the Souken platform. Implements {rng.choice(['CQRS', 'Event Sourcing', 'Saga', 'Circuit Breaker'])}")
    lines.append(f" * pattern for resilient operation.</p>")
    lines.append(f" *")
    lines.append(f" * @author {rng.choice(TEAM_MEMBERS)}")
    lines.append(f" * @since {fake_version(rng)}")
    lines.append(f" * @see {rfc_ref(rng)}")
    lines.append(f" */")
    if rng.random() < 0.5:
        lines.append(f"@Singleton")
    lines.append(f"public class {full_name} {{")
    lines.append(f"")

    lines.append(f"    private static final Logger LOGGER = Logger.getLogger({full_name}.class.getName());")
    lines.append(f"    private static final int MAX_{rng.choice(ENT_NOUNS).upper()}_CAPACITY = {rng.choice([64, 128, 256, 512, 1024, 4096])};")
    lines.append(f"    private static final Duration DEFAULT_TIMEOUT = Duration.ofMillis({rng.choice([100, 250, 500, 1000, 5000])});")
    lines.append(f"")

    # fields
    fields = []
    for _ in range(rng.randint(3, 7)):
        fname = _camel(ALL_NOUNS, rng)
        ftype = _java_type(rng)
        lines.append(f"    private final {ftype} {fname};")
        fields.append(fname)
    lines.append(f"    private final ConcurrentHashMap<String, Object> stateMap;")
    lines.append(f"    private final AtomicLong invocationCounter;")
    lines.append(f"")

    # constructor
    params = ", ".join(f"{_java_type(rng)} {f}" for f in fields[:3])
    lines.append(f"    @Inject")
    lines.append(f"    public {full_name}({params}) {{")
    for f in fields[:3]:
        lines.append(f"        this.{f} = {f};")
    for f in fields[3:]:
        lines.append(f"        this.{f} = null;")
    lines.append(f"        this.stateMap = new ConcurrentHashMap<>();")
    lines.append(f"        this.invocationCounter = new AtomicLong(0);")
    lines.append(f'        LOGGER.info("{full_name} initialized");')
    lines.append(f"    }}")
    lines.append(f"")

    # methods
    for _ in range(rng.randint(3, 8)):
        mname = _camel(ENT_VERBS, rng) + _pascal(ALL_NOUNS, rng)
        mparams = []
        for _ in range(rng.randint(1, 4)):
            mparams.append(f"final {_java_type(rng)} {_camel(ALL_NOUNS, rng)}")
        mparam_str = ", ".join(mparams)
        ret = _java_type(rng)

        lines.append(f"    /**")
        lines.append(f"     * {mname} — {rng.choice(ENT_VERBS).replace('_', ' ')} the {rng.choice(ENT_NOUNS).replace('_', ' ')}.")
        lines.append(f"     * Tracking: {ticket(rng)}")
        lines.append(f"     */")
        lines.append(f"    {_annotation(rng)}")
        lines.append(f"    public {ret} {mname}({mparam_str}) throws Exception {{")
        lines.append(f"        final long startNanos = System.nanoTime();")
        lines.append(f"        invocationCounter.incrementAndGet();")
        lines.append(f"")
        lines.append(f'        LOGGER.fine(() -> String.format("{mname}: invocation #%d", invocationCounter.get()));')
        lines.append(f"")

        for _ in range(rng.randint(2, 5)):
            var = _camel(ALL_NOUNS, rng)
            val = rng.choice([
                "UUID.randomUUID().toString()",
                "Instant.now()",
                "stateMap.size()",
                f"Math.log1p({rng.uniform(0, 100):.4f})",
                "Collections.emptyMap()",
                "Optional.empty()",
                f'"{rng.choice(ENT_NOUNS)}"',
            ])
            lines.append(f"        final var {var} = {val};")

        lines.append(f"")
        lines.append(f"        // TODO({rng.choice(TEAM_MEMBERS)}): Optimize for high-throughput scenarios")
        lines.append(f"        final long elapsedNanos = System.nanoTime() - startNanos;")
        lines.append(f'        stateMap.put("{mname}.lastDuration", Duration.ofNanos(elapsedNanos));')
        lines.append(f"        return null;")
        lines.append(f"    }}")
        lines.append(f"")

    lines.append(f"}}")
    lines.append(f"")
    return lines


def generate_java_file(module_path, target_lines, rng):
    class_name = _pascal(ALL_NOUNS, rng) + rng.choice(["Service", "Manager", "Handler"])
    lines = gen_header(module_path, class_name, rng)

    if rng.random() < 0.3:
        lines.extend(gen_interface(rng))

    if rng.random() < 0.3:
        lines.extend(gen_enum(rng))

    while len(lines) < target_lines:
        lines.extend(gen_class(rng))

    return "\n".join(lines[:target_lines])
