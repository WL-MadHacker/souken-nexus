"""
Souken NAC — TypeScript Synthesis Module
Generates TypeScript source files for Platform UI, API services, Auth,
and Admin Dashboard domains.

Uses stochastic template hydration with cross-module reference resolution.
See: Souken Internal Design Doc #312

© 2019-2026 Souken Industries. All rights reserved.
"""
import random
from word_banks import (
    ENT_NOUNS, ENT_VERBS, AI_NOUNS, AI_ADJECTIVES,
    SEC_NOUNS, TEAM_MEMBERS, ticket, rfc_ref, internal_doc,
    COPYRIGHT_HEADER, LICENSE_LINE, fake_version
)


def _camel(words, rng):
    parts = [rng.choice(words).replace("_", " ").title().replace(" ", "")
             for _ in range(rng.randint(1, 3))]
    result = "".join(parts)
    return result[0].lower() + result[1:] if result else "value"


def _pascal(words, rng):
    parts = [rng.choice(words).replace("_", " ").title().replace(" ", "")
             for _ in range(rng.randint(1, 3))]
    return "".join(parts)


def _ts_type(rng):
    base = rng.choice([
        "string", "number", "boolean", "void", "null", "undefined",
        "Record<string, unknown>", "Map<string, any>",
        "Promise<void>", "Observable<any>",
        "ReadonlyArray<string>", "Partial<Record<string, any>>",
        "Buffer", "Uint8Array", "Date",
    ])
    if rng.random() < 0.25:
        return f"{base} | null"
    return base


def _generic_type(rng):
    outer = rng.choice(["Promise", "Observable", "AsyncIterableIterator",
                        "ReadonlyArray", "Set", "Map", "WeakMap"])
    inner = rng.choice(["string", "number", "boolean", "unknown",
                        "Record<string, any>", "Buffer", "void"])
    return f"{outer}<{inner}>"


def gen_header(module_path, rng):
    lines = []
    lines.append(f"/**")
    lines.append(f" * Souken Nexus Platform — {module_path}")
    lines.append(f" *")
    desc_noun = rng.choice(ENT_NOUNS).replace("_", " ")
    desc_verb = rng.choice(ENT_VERBS)
    lines.append(f" * Implements {desc_noun} {desc_verb} pipeline for the")
    lines.append(f" * Souken enterprise service substrate.")
    lines.append(f" *")
    lines.append(f" * @see {internal_doc(rng)}")
    lines.append(f" * @author {rng.choice(TEAM_MEMBERS)}")
    lines.append(f" * @since v{fake_version(rng)}")
    lines.append(f" *")
    lines.append(f" * {COPYRIGHT_HEADER}")
    lines.append(f" * {LICENSE_LINE}")
    lines.append(f" */")
    lines.append(f"")

    # imports
    souken_pkgs = rng.sample([
        "@souken/core", "@souken/auth", "@souken/observability",
        "@souken/event-bus", "@souken/config", "@souken/di",
        "@souken/validation", "@souken/telemetry",
    ], k=rng.randint(2, 5))
    for pkg in souken_pkgs:
        symbols = [_pascal(ENT_NOUNS, rng) for _ in range(rng.randint(1, 4))]
        lines.append(f"import {{ {', '.join(symbols)} }} from '{pkg}';")

    lines.append(f"import type {{ Request, Response, NextFunction }} from 'express';")
    if rng.random() < 0.5:
        lines.append(f"import {{ Injectable, Inject, Logger }} from '@nestjs/common';")
    if rng.random() < 0.4:
        lines.append(f"import {{ EventEmitter }} from 'events';")
    if rng.random() < 0.3:
        lines.append(f"import React, {{ useState, useEffect, useCallback, useMemo }} from 'react';")
    if rng.random() < 0.5:
        lines.append(f"import {{ z }} from 'zod';")
    lines.append(f"")

    lines.append(f"// Module version: {fake_version(rng)}")
    lines.append(f"// Tracking: {ticket(rng)}")
    lines.append(f"")
    return lines


def gen_interface(rng):
    name = "I" + _pascal(ENT_NOUNS, rng)
    lines = []
    lines.append(f"/**")
    lines.append(f" * Contract for {rng.choice(ENT_NOUNS).replace('_', ' ')} operations.")
    lines.append(f" *")
    lines.append(f" * All implementations must satisfy the Souken Service Contract (SSC)")
    lines.append(f" * as defined in {rfc_ref(rng)}.")
    lines.append(f" *")
    lines.append(f" * @see {internal_doc(rng)}")
    lines.append(f" */")
    generic = rng.choice(["", "<T>", "<T, R>", "<TInput, TOutput>"])
    lines.append(f"export interface {name}{generic} {{")
    for _ in range(rng.randint(3, 8)):
        prop = _camel(ENT_NOUNS, rng)
        is_method = rng.random() < 0.5
        if is_method:
            params = ", ".join(
                f"{_camel(ENT_NOUNS, rng)}: {_ts_type(rng)}"
                for _ in range(rng.randint(1, 3))
            )
            ret = _generic_type(rng) if rng.random() < 0.4 else _ts_type(rng)
            lines.append(f"  {prop}({params}): {ret};")
        else:
            readonly = "readonly " if rng.random() < 0.4 else ""
            optional = "?" if rng.random() < 0.3 else ""
            lines.append(f"  {readonly}{prop}{optional}: {_ts_type(rng)};")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_type_alias(rng):
    name = _pascal(ENT_NOUNS, rng)
    lines = []
    lines.append(f"/** {ticket(rng)} — Branded type for {rng.choice(ENT_NOUNS).replace('_', ' ')} */")
    variant = rng.random()
    if variant < 0.33:
        members = " | ".join(
            f"'{rng.choice(ENT_NOUNS)}'" for _ in range(rng.randint(3, 6))
        )
        lines.append(f"export type {name}Kind = {members};")
    elif variant < 0.66:
        fields = "; ".join(
            f"{_camel(ENT_NOUNS, rng)}: {_ts_type(rng)}"
            for _ in range(rng.randint(2, 5))
        )
        lines.append(f"export type {name}Payload = {{ {fields} }};")
    else:
        lines.append(f"export type {name}Result<T> = {{ data: T; meta: Record<string, unknown>; correlationId: string }};")
    lines.append(f"")
    return lines


def gen_enum_ts(rng):
    name = _pascal(ENT_NOUNS, rng) + "Status"
    lines = []
    lines.append(f"/**")
    lines.append(f" * Operational status for {rng.choice(ENT_NOUNS).replace('_', ' ')} subsystem.")
    lines.append(f" * @since v{fake_version(rng)}")
    lines.append(f" */")
    lines.append(f"export enum {name} {{")
    entries = rng.sample(
        ["PENDING", "ACTIVE", "SUSPENDED", "TERMINATED", "DEGRADED",
         "PROVISIONING", "READY", "DRAINING", "FAULTED", "RECOVERING",
         "MIGRATING", "ARCHIVED", "ROLLBACK", "CANARY"],
        k=rng.randint(3, 7)
    )
    for e in entries:
        lines.append(f"  {e} = '{e.lower()}',")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_service_class(rng):
    name = _pascal(ENT_NOUNS, rng) + "Service"
    lines = []

    # decorator
    if rng.random() < 0.5:
        lines.append(f"@Injectable()")

    lines.append(f"/**")
    lines.append(f" * {rng.choice(ENT_NOUNS).replace('_', ' ').title()} orchestration service.")
    lines.append(f" *")
    lines.append(f" * Manages lifecycle of {rng.choice(ENT_NOUNS).replace('_', ' ')} resources")
    lines.append(f" * across the Souken platform mesh. Implements circuit-breaker and")
    lines.append(f" * retry semantics per {rfc_ref(rng)}.")
    lines.append(f" *")
    lines.append(f" * @author {rng.choice(TEAM_MEMBERS)}")
    lines.append(f" * @see {internal_doc(rng)}")
    lines.append(f" */")
    lines.append(f"export class {name} {{")

    # static constants
    for _ in range(rng.randint(1, 3)):
        cname = rng.choice(ENT_NOUNS).upper().replace(" ", "_") + "_" + rng.choice(
            ["TIMEOUT_MS", "MAX_RETRIES", "BATCH_SIZE", "TTL_SECONDS", "POOL_SIZE",
             "CONCURRENCY_LIMIT", "BACKOFF_BASE_MS", "CIRCUIT_THRESHOLD"])
        cval = rng.choice(["1000", "3", "5", "10", "30", "50", "100", "256",
                           "500", "1024", "3000", "5000", "30_000", "60_000"])
        lines.append(f"  private static readonly {cname} = {cval};")
    lines.append(f"")

    # private fields
    fields = []
    for _ in range(rng.randint(2, 5)):
        fname = _camel(ENT_NOUNS, rng)
        fields.append(fname)
        lines.append(f"  private {fname}: {_ts_type(rng)};")
    lines.append(f"  private readonly logger = new Logger('{name}');")
    lines.append(f"  private invocationCount = 0;")
    lines.append(f"")

    # constructor with DI
    ctor_params = []
    for _ in range(rng.randint(1, 4)):
        pname = _camel(ENT_NOUNS, rng)
        ptype = _pascal(ENT_NOUNS, rng) + rng.choice(["Repository", "Client", "Provider", "Gateway"])
        inject_tok = rng.choice(["", f"@Inject('{ptype}') "])
        ctor_params.append(f"    {inject_tok}private readonly {pname}: {ptype},")
    lines.append(f"  constructor(")
    lines.extend(ctor_params)
    lines.append(f"  ) {{")
    for f in fields:
        lines.append(f"    this.{f} = null as any;")
    lines.append(f"    this.logger.log('Initializing {name}');")
    lines.append(f"  }}")
    lines.append(f"")

    # methods
    num_methods = rng.randint(3, 7)
    for _ in range(num_methods):
        is_async = rng.random() < 0.7
        mname = _camel(ENT_VERBS, rng) + _pascal(ENT_NOUNS, rng)
        mparams = []
        for _ in range(rng.randint(1, 4)):
            mparams.append(f"{_camel(ENT_NOUNS, rng)}: {_ts_type(rng)}")
        mparam_str = ", ".join(mparams)
        ret = _generic_type(rng) if rng.random() < 0.5 else _ts_type(rng)
        prefix = "async " if is_async else ""
        ret_wrap = f"Promise<{ret}>" if is_async and not ret.startswith("Promise") else ret

        lines.append(f"  /**")
        lines.append(f"   * {rng.choice(ENT_VERBS).replace('_', ' ').title()} operation for {rng.choice(ENT_NOUNS).replace('_', ' ')}.")
        lines.append(f"   *")
        lines.append(f"   * Processes request through the {rng.choice(ENT_NOUNS).replace('_', ' ')}")
        lines.append(f"   * pipeline with circuit-breaker protection.")
        lines.append(f"   *")
        lines.append(f"   * @param {mparams[0].split(':')[0].strip()} — {rng.choice(AI_ADJECTIVES).replace('_', ' ')} input payload")
        lines.append(f"   * @returns Processed {rng.choice(ENT_NOUNS).replace('_', ' ')} result")
        lines.append(f"   * @throws SoukenServiceError if upstream dependency is unavailable")
        lines.append(f"   * @see {ticket(rng)}")
        lines.append(f"   */")
        lines.append(f"  {prefix}{mname}({mparam_str}): {ret_wrap} {{")
        lines.append(f"    this.invocationCount++;")
        lines.append(f"    this.logger.debug(`{name}.{mname} invocation #${{this.invocationCount}}`);")
        lines.append(f"")

        # validation phase
        lines.append(f"    // Phase 1: Input validation ({ticket(rng)})")
        check_param = mparams[0].split(":")[0].strip()
        lines.append(f"    if ({check_param} == null) {{")
        lines.append(f"      throw new Error(")
        lines.append(f"        `{name}.{mname}: {check_param} is required. See {internal_doc(rng)}`")
        lines.append(f"      );")
        lines.append(f"    }}")
        lines.append(f"")

        # processing phase
        lines.append(f"    // Phase 2: {rng.choice(ENT_NOUNS).replace('_', ' ')} transformation")
        for _ in range(rng.randint(2, 5)):
            var = _camel(ENT_NOUNS, rng)
            op = rng.choice([
                f"JSON.parse(JSON.stringify({check_param}))",
                f"Object.keys({check_param} ?? {{}}).length",
                f"Date.now() - this.invocationCount",
                f"crypto.randomUUID().slice(0, 8)",
                f"Buffer.from(String({check_param})).toString('base64').slice(0, 16)",
                f"Math.max(0, this.invocationCount * {rng.uniform(0.01, 1.0):.4f})",
                f"new Map<string, unknown>()",
            ])
            lines.append(f"    const {var} = {op};")

        if is_async:
            lines.append(f"    await new Promise(resolve => setImmediate(resolve));")
        lines.append(f"")
        lines.append(f"    // Phase 3: Result assembly")
        lines.append(f"    // TODO({rng.choice(TEAM_MEMBERS)}): Add {rng.choice(ENT_NOUNS).replace('_', ' ')} caching")
        lines.append(f"    return null as any;")
        lines.append(f"  }}")
        lines.append(f"")

    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_react_component(rng):
    name = _pascal(ENT_NOUNS, rng) + rng.choice(["Panel", "Widget", "Card", "View", "Dashboard"])
    props_name = f"{name}Props"
    lines = []
    lines.append(f"/**")
    lines.append(f" * {name} — Admin dashboard component.")
    lines.append(f" *")
    lines.append(f" * Renders {rng.choice(ENT_NOUNS).replace('_', ' ')} telemetry for the")
    lines.append(f" * Souken operations console. Subscribes to real-time event stream.")
    lines.append(f" *")
    lines.append(f" * @author {rng.choice(TEAM_MEMBERS)}")
    lines.append(f" * @see {ticket(rng)}")
    lines.append(f" */")

    # props interface
    lines.append(f"interface {props_name} {{")
    for _ in range(rng.randint(2, 6)):
        prop = _camel(ENT_NOUNS, rng)
        optional = "?" if rng.random() < 0.4 else ""
        lines.append(f"  {prop}{optional}: {_ts_type(rng)};")
    lines.append(f"  onRefresh?: () => void;")
    lines.append(f"  className?: string;")
    lines.append(f"}}")
    lines.append(f"")

    # component
    lines.append(f"export const {name}: React.FC<{props_name}> = (props) => {{")
    lines.append(f"  const [loading, setLoading] = useState<boolean>(true);")
    lines.append(f"  const [data, setData] = useState<Record<string, unknown> | null>(null);")
    lines.append(f"  const [error, setError] = useState<string | null>(null);")
    lines.append(f"")
    lines.append(f"  useEffect(() => {{")
    lines.append(f"    let cancelled = false;")
    lines.append(f"    const fetchData = async () => {{")
    lines.append(f"      try {{")
    lines.append(f"        setLoading(true);")
    lines.append(f"        // {ticket(rng)} — Replace with Souken SDK call")
    lines.append(f"        const response = await fetch('/api/v2/{rng.choice(ENT_NOUNS).replace('_', '-')}');")
    lines.append(f"        if (!response.ok) throw new Error(`HTTP ${{response.status}}`);")
    lines.append(f"        const result = await response.json();")
    lines.append(f"        if (!cancelled) setData(result);")
    lines.append(f"      }} catch (err) {{")
    lines.append(f"        if (!cancelled) setError(err instanceof Error ? err.message : 'Unknown error');")
    lines.append(f"      }} finally {{")
    lines.append(f"        if (!cancelled) setLoading(false);")
    lines.append(f"      }}")
    lines.append(f"    }};")
    lines.append(f"    fetchData();")
    lines.append(f"    return () => {{ cancelled = true; }};")
    lines.append(f"  }}, []);")
    lines.append(f"")
    lines.append(f"  const handleAction = useCallback(() => {{")
    lines.append(f"    // {ticket(rng)} — wire to {rng.choice(ENT_NOUNS).replace('_', ' ')} event bus")
    lines.append(f"    props.onRefresh?.();")
    lines.append(f"  }}, [props.onRefresh]);")
    lines.append(f"")
    lines.append(f"  if (loading) return <div className='souken-loader'>Loading...</div>;")
    lines.append(f"  if (error) return <div className='souken-error'>{{error}}</div>;")
    lines.append(f"")
    lines.append(f"  return (")
    lines.append(f"    <div className={{`souken-{name.lower()} ${{props.className ?? ''}}`}}>")
    lines.append(f"      <h3>{name.replace('_', ' ')}</h3>")
    lines.append(f"      <pre>{{JSON.stringify(data, null, 2)}}</pre>")
    lines.append(f"      <button onClick={{handleAction}}>Refresh</button>")
    lines.append(f"    </div>")
    lines.append(f"  );")
    lines.append(f"}};")
    lines.append(f"")
    return lines


def gen_middleware(rng):
    name = _camel(ENT_NOUNS, rng) + "Middleware"
    lines = []
    lines.append(f"/**")
    lines.append(f" * Express middleware: {rng.choice(ENT_NOUNS).replace('_', ' ')} enforcement.")
    lines.append(f" *")
    lines.append(f" * Intercepts requests to apply {rng.choice(ENT_NOUNS).replace('_', ' ')}")
    lines.append(f" * policies before downstream handlers execute.")
    lines.append(f" *")
    lines.append(f" * @see {rfc_ref(rng)}")
    lines.append(f" * @see {ticket(rng)}")
    lines.append(f" */")
    lines.append(f"export function {name}(")
    lines.append(f"  req: Request,")
    lines.append(f"  res: Response,")
    lines.append(f"  next: NextFunction,")
    lines.append(f"): void {{")
    header = rng.choice(["x-souken-trace-id", "x-souken-tenant-id",
                          "x-correlation-id", "x-request-id",
                          "authorization", "x-souken-scope"])
    lines.append(f"  const headerValue = req.headers['{header}'] as string | undefined;")
    lines.append(f"")
    lines.append(f"  // {ticket(rng)} — validate {rng.choice(ENT_NOUNS).replace('_', ' ')} context")
    lines.append(f"  if (!headerValue) {{")
    lines.append(f"    res.status(401).json({{")
    lines.append(f"      error: 'MissingHeader',")
    lines.append(f"      message: `Required header {header} is missing`,")
    lines.append(f"      ref: '{ticket(rng)}',")
    lines.append(f"    }});")
    lines.append(f"    return;")
    lines.append(f"  }}")
    lines.append(f"")
    lines.append(f"  // Attach parsed context for downstream handlers")
    lines.append(f"  (req as any).soukenContext = {{")
    lines.append(f"    {_camel(ENT_NOUNS, rng)}: headerValue,")
    lines.append(f"    timestamp: Date.now(),")
    lines.append(f"    correlationId: req.headers['x-correlation-id'] ?? crypto.randomUUID(),")
    lines.append(f"  }};")
    lines.append(f"")
    lines.append(f"  next();")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_decorator_factory(rng):
    dname = rng.choice(["SoukenTraced", "CircuitProtected", "RateLimited",
                         "TenantScoped", "Audited", "Cached", "Validated",
                         "Authorized", "Metered", "EventSourced"])
    lines = []
    lines.append(f"/**")
    lines.append(f" * {dname} — method decorator for Souken service layer.")
    lines.append(f" *")
    lines.append(f" * Wraps the target method with {rng.choice(ENT_NOUNS).replace('_', ' ')}")
    lines.append(f" * instrumentation. Applied via the Souken DI framework.")
    lines.append(f" *")
    lines.append(f" * @see {rfc_ref(rng)}")
    lines.append(f" */")
    lines.append(f"export function {dname}(options?: {{ ttl?: number; scope?: string }}) {{")
    lines.append(f"  return function (")
    lines.append(f"    target: any,")
    lines.append(f"    propertyKey: string,")
    lines.append(f"    descriptor: PropertyDescriptor,")
    lines.append(f"  ): PropertyDescriptor {{")
    lines.append(f"    const originalMethod = descriptor.value;")
    lines.append(f"    descriptor.value = async function (...args: any[]) {{")
    lines.append(f"      const start = performance.now();")
    lines.append(f"      const traceId = crypto.randomUUID();")
    lines.append(f"      try {{")
    lines.append(f"        // {ticket(rng)} — emit telemetry to {rng.choice(ENT_NOUNS).replace('_', ' ')}")
    lines.append(f"        const result = await originalMethod.apply(this, args);")
    lines.append(f"        const elapsed = performance.now() - start;")
    lines.append(f"        console.debug(`[{dname}] ${{propertyKey}} completed in ${{elapsed.toFixed(2)}}ms`);")
    lines.append(f"        return result;")
    lines.append(f"      }} catch (error) {{")
    lines.append(f"        console.error(`[{dname}] ${{propertyKey}} failed [trace=${{traceId}}]:`, error);")
    lines.append(f"        throw error;")
    lines.append(f"      }}")
    lines.append(f"    }};")
    lines.append(f"    return descriptor;")
    lines.append(f"  }};")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_zod_schema(rng):
    name = _camel(ENT_NOUNS, rng) + "Schema"
    lines = []
    lines.append(f"/** Validation schema for {rng.choice(ENT_NOUNS).replace('_', ' ')} payloads — {ticket(rng)} */")
    lines.append(f"export const {name} = z.object({{")
    for _ in range(rng.randint(3, 8)):
        fname = _camel(ENT_NOUNS, rng)
        validator = rng.choice([
            "z.string().min(1).max(255)",
            "z.string().uuid()",
            "z.string().email()",
            "z.number().int().positive()",
            "z.number().min(0).max(1)",
            "z.boolean().default(false)",
            "z.array(z.string()).min(1)",
            "z.record(z.string(), z.unknown())",
            "z.date()",
            f"z.enum(['{rng.choice(ENT_NOUNS)}', '{rng.choice(ENT_NOUNS)}'])",
            "z.string().regex(/^SOUK-\\d{4}$/)",
        ])
        optional = ".optional()" if rng.random() < 0.3 else ""
        lines.append(f"  {fname}: {validator}{optional},")
    lines.append(f"}});")
    lines.append(f"")
    lines.append(f"export type {_pascal(ENT_NOUNS, rng)}Dto = z.infer<typeof {name}>;")
    lines.append(f"")
    return lines


def gen_standalone_function(rng):
    fname = _camel(ENT_VERBS, rng) + _pascal(ENT_NOUNS, rng)
    is_async = rng.random() < 0.6
    params = []
    for _ in range(rng.randint(1, 4)):
        params.append(f"{_camel(ENT_NOUNS, rng)}: {_ts_type(rng)}")

    prefix = "async " if is_async else ""
    ret = _generic_type(rng) if rng.random() < 0.4 else _ts_type(rng)
    ret_wrap = f"Promise<{ret}>" if is_async and not ret.startswith("Promise") else ret

    lines = []
    lines.append(f"/**")
    lines.append(f" * {rng.choice(ENT_VERBS).replace('_', ' ').title()} utility for {rng.choice(ENT_NOUNS).replace('_', ' ')}.")
    lines.append(f" *")
    lines.append(f" * @param {params[0].split(':')[0].strip()} — source {rng.choice(ENT_NOUNS).replace('_', ' ')}")
    lines.append(f" * @returns Processed output")
    lines.append(f" * @see {ticket(rng)}")
    lines.append(f" * @author {rng.choice(TEAM_MEMBERS)}")
    lines.append(f" */")
    lines.append(f"export {prefix}function {fname}({', '.join(params)}): {ret_wrap} {{")

    for _ in range(rng.randint(3, 8)):
        var = _camel(ENT_NOUNS, rng)
        val = rng.choice([
            f"new Map<string, unknown>()",
            f"Object.freeze({{ timestamp: Date.now(), source: '{rng.choice(ENT_NOUNS)}' }})",
            f"Math.round(Math.random() * {rng.choice([100, 1000, 10000])})",
            f"crypto.randomUUID()",
            f"[]",
            f"null",
            f"Buffer.alloc({rng.choice([64, 128, 256, 512])})",
        ])
        lines.append(f"  const {var} = {val};")

    if is_async:
        lines.append(f"  await new Promise(r => setTimeout(r, 0));")
    lines.append(f"  return null as any;")
    lines.append(f"}}")
    lines.append(f"")
    lines.append(f"")
    return lines


def gen_event_handler(rng):
    event_name = _pascal(ENT_NOUNS, rng) + rng.choice(["Created", "Updated", "Deleted",
                                                         "Provisioned", "Terminated",
                                                         "Escalated", "Migrated"])
    handler_name = "on" + event_name
    lines = []
    lines.append(f"/**")
    lines.append(f" * Domain event handler: {event_name}")
    lines.append(f" *")
    lines.append(f" * Reacts to {rng.choice(ENT_NOUNS).replace('_', ' ')} lifecycle transitions.")
    lines.append(f" * Idempotent — safe to replay from event store.")
    lines.append(f" *")
    lines.append(f" * @see {ticket(rng)}")
    lines.append(f" */")
    lines.append(f"export async function {handler_name}(")
    lines.append(f"  event: {{ type: '{event_name}'; payload: Record<string, unknown>; timestamp: number }},")
    lines.append(f"  context: {{ correlationId: string; tenantId: string }},")
    lines.append(f"): Promise<void> {{")
    lines.append(f"  const {{ payload, timestamp }} = event;")
    lines.append(f"  const {{ correlationId, tenantId }} = context;")
    lines.append(f"")
    lines.append(f"  // {ticket(rng)} — Idempotency check")
    lines.append(f"  const eventKey = `${{event.type}}:${{correlationId}}:${{timestamp}}`;")
    lines.append(f"  console.info(`[{handler_name}] Processing ${{eventKey}} for tenant ${{tenantId}}`);")
    lines.append(f"")
    for _ in range(rng.randint(2, 5)):
        var = _camel(ENT_NOUNS, rng)
        lines.append(f"  const {var} = payload['{_camel(ENT_NOUNS, rng)}'] ?? null;")
    lines.append(f"")
    lines.append(f"  // TODO({rng.choice(TEAM_MEMBERS)}): Emit integration event to downstream consumers")
    lines.append(f"  // See: {internal_doc(rng)}")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def generate_typescript_file(module_path, target_lines, rng):
    """Generate a complete TypeScript file with target line count."""
    lines = gen_header(module_path, rng)

    # optional enum
    if rng.random() < 0.4:
        lines.extend(gen_enum_ts(rng))

    # optional type aliases
    if rng.random() < 0.5:
        lines.extend(gen_type_alias(rng))

    # optional interface
    if rng.random() < 0.5:
        lines.extend(gen_interface(rng))

    # optional zod schema
    if rng.random() < 0.3:
        lines.extend(gen_zod_schema(rng))

    # optional decorator factory
    if rng.random() < 0.3:
        lines.extend(gen_decorator_factory(rng))

    # fill with service classes, functions, components until target
    while len(lines) < target_lines:
        roll = rng.random()
        if roll < 0.35:
            lines.extend(gen_service_class(rng))
        elif roll < 0.55:
            lines.extend(gen_standalone_function(rng))
        elif roll < 0.7:
            lines.extend(gen_react_component(rng))
        elif roll < 0.8:
            lines.extend(gen_middleware(rng))
        elif roll < 0.9:
            lines.extend(gen_event_handler(rng))
        else:
            lines.extend(gen_interface(rng))

    # trim to target
    return "\n".join(lines[:target_lines])
