"""
Souken NAC — Rust Synthesis Module
Generates Rust source files for runtime engine, consensus, inference,
service mesh, and real-time event system domains.

Uses stochastic template hydration with cross-module reference resolution.
See: Souken Internal Design Doc #312

© 2019-2026 Souken Industries. All rights reserved.
"""
import random
from word_banks import (
    AI_NOUNS, AI_VERBS, AI_ADJECTIVES, DIST_NOUNS, DIST_VERBS,
    ENT_NOUNS, ENT_VERBS, SEC_NOUNS, TEAM_MEMBERS,
    ticket, rfc_ref, internal_doc, COPYRIGHT_HEADER, LICENSE_LINE, fake_version,
)


def _snake(words, rng):
    return "_".join(rng.choice(words) for _ in range(rng.randint(1, 3)))


def _type_name(words, rng):
    parts = [rng.choice(words).replace("_", " ").title().replace(" ", "")
             for _ in range(rng.randint(1, 3))]
    return "".join(parts)


def _rust_type(rng):
    base = rng.choice([
        "u8", "u16", "u32", "u64", "usize", "i32", "i64",
        "f32", "f64", "bool", "String", "&str", "&[u8]",
        "Vec<u8>", "Vec<f64>", "Vec<String>",
        "HashMap<String, Value>", "BTreeMap<String, f64>",
        "Arc<Mutex<Self>>", "Arc<RwLock<Vec<u8>>>",
        "Box<dyn Error + Send + Sync>",
        "Pin<Box<dyn Future<Output = ()> + Send>>",
        "Sender<PipelineMessage>", "Receiver<ConsensusEvent>",
    ])
    if rng.random() < 0.25:
        return f"Option<{base}>"
    if rng.random() < 0.2:
        return f"Result<{base}, SoukenError>"
    return base


def _lifetime(rng):
    return rng.choice(["'a", "'b", "'ctx", "'req", "'conn", "'static"])


def _derive_macros(rng):
    pool = ["Debug", "Clone", "Default", "PartialEq", "Eq", "Hash",
            "Serialize", "Deserialize", "PartialOrd", "Ord"]
    count = rng.randint(2, 6)
    chosen = rng.sample(pool, min(count, len(pool)))
    return ", ".join(chosen)


_FAKE_CRATES = [
    "souken_core", "souken_nexus", "souken_runtime", "souken_consensus",
    "souken_inference", "souken_mesh", "souken_telemetry", "souken_crypto",
    "souken_events", "souken_proto", "souken_storage", "souken_graph",
]

_FAKE_MODULES = [
    "engine", "pipeline", "scheduler", "allocator", "codec",
    "transport", "protocol", "handler", "dispatcher", "resolver",
    "registry", "validator", "transformer", "coordinator", "broker",
]


def gen_header(module_path, rng):
    lines = []
    lines.append(f"// {COPYRIGHT_HEADER}")
    lines.append(f"// {LICENSE_LINE}")
    lines.append(f"//")
    lines.append(f"// Souken Nexus Platform — {module_path}")
    desc_parts = [rng.choice(AI_ADJECTIVES), rng.choice(DIST_NOUNS), rng.choice(AI_VERBS)]
    lines.append(f"// Implements {desc_parts[0]} {desc_parts[1]} {desc_parts[2]} subsystem")
    lines.append(f"// for the Souken distributed cognitive runtime.")
    lines.append(f"//")
    lines.append(f"// Ref: {internal_doc(rng)}")
    lines.append(f"// Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"// Since: v{fake_version(rng)}")
    lines.append(f"")

    # file-level attributes
    allow_items = rng.sample([
        "dead_code", "unused_imports", "unused_variables",
        "clippy::too_many_arguments", "clippy::module_inception",
        "clippy::needless_lifetimes", "clippy::redundant_closure",
    ], rng.randint(2, 4))
    deny_items = rng.sample([
        "unsafe_op_in_unsafe_fn", "missing_debug_implementations",
        "unreachable_pub", "unused_must_use",
    ], rng.randint(1, 3))
    lines.append(f"#![allow({', '.join(allow_items)})]")
    lines.append(f"#![deny({', '.join(deny_items)})]")
    lines.append(f"")

    # use statements
    num_uses = rng.randint(4, 10)
    for _ in range(num_uses):
        crate = rng.choice(_FAKE_CRATES)
        mod = rng.choice(_FAKE_MODULES)
        item = _type_name(AI_NOUNS + DIST_NOUNS, rng)
        lines.append(f"use {crate}::{mod}::{{{item}}};")
    lines.append(f"")

    std_imports = [
        "use std::collections::{HashMap, BTreeMap, HashSet};",
        "use std::sync::{Arc, Mutex, RwLock};",
        "use std::fmt;",
    ]
    if rng.random() < 0.6:
        std_imports.append("use std::pin::Pin;")
    if rng.random() < 0.6:
        std_imports.append("use std::future::Future;")
    if rng.random() < 0.5:
        std_imports.append("use std::io::{self, Read, Write};")
    if rng.random() < 0.5:
        std_imports.append("use tokio::sync::{mpsc, oneshot, broadcast};")
    if rng.random() < 0.4:
        std_imports.append("use tracing::{debug, info, warn, error, instrument};")
    if rng.random() < 0.3:
        std_imports.append("use serde::{Serialize, Deserialize};")
    for imp in std_imports:
        lines.append(imp)
    lines.append(f"")

    lines.append(f"/// Module version: {fake_version(rng)}")
    lines.append(f"/// Tracking: {ticket(rng)}")
    lines.append(f"")
    return lines


def gen_enum(rng):
    name = _type_name(DIST_NOUNS + AI_NOUNS, rng) + "Kind"
    lines = []
    lines.append(f"/// Operational variants for the {rng.choice(AI_ADJECTIVES)} {rng.choice(DIST_NOUNS)} subsystem.")
    lines.append(f"/// See: {rfc_ref(rng)}")
    lines.append(f"#[derive({_derive_macros(rng)})]")
    lines.append(f"pub enum {name} {{")
    for _ in range(rng.randint(3, 8)):
        variant = _type_name(DIST_NOUNS + AI_NOUNS, rng)
        if rng.random() < 0.4:
            inner = _rust_type(rng)
            lines.append(f"    /// {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} variant.")
            lines.append(f"    {variant}({inner}),")
        elif rng.random() < 0.3:
            fields = []
            for _ in range(rng.randint(2, 4)):
                fname = _snake(DIST_NOUNS, rng)
                ftype = _rust_type(rng)
                fields.append(f"        {fname}: {ftype},")
            lines.append(f"    /// Structured variant for {rng.choice(AI_NOUNS)} state.")
            lines.append(f"    {variant} {{")
            lines.extend(fields)
            lines.append(f"    }},")
        else:
            lines.append(f"    /// Unit variant — {rng.choice(AI_VERBS)} mode.")
            lines.append(f"    {variant},")
    lines.append(f"}}")
    lines.append(f"")
    lines.append(f"")
    return lines


def gen_struct(rng):
    name = _type_name(AI_NOUNS + DIST_NOUNS, rng)
    has_lifetime = rng.random() < 0.25
    lt = f"<{_lifetime(rng)}>" if has_lifetime else ""
    lines = []
    lines.append(f"/// {rng.choice(AI_ADJECTIVES).replace('_', '-').title()} {rng.choice(DIST_NOUNS).replace('_', ' ')} component.")
    lines.append(f"///")
    lines.append(f"/// Orchestrates {rng.choice(AI_ADJECTIVES)} {rng.choice(AI_NOUNS)} operations")
    lines.append(f"/// across the Souken distributed cognitive substrate.")
    lines.append(f"/// Implements the protocol defined in {rfc_ref(rng)}.")
    lines.append(f"///")
    lines.append(f"/// Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"#[derive({_derive_macros(rng)})]")
    lines.append(f"pub struct {name}{lt} {{")
    field_names = []
    for _ in range(rng.randint(3, 10)):
        fname = _snake(AI_NOUNS + DIST_NOUNS, rng)
        ftype = _rust_type(rng)
        lines.append(f"    /// {rng.choice(AI_ADJECTIVES).replace('_', ' ')} {rng.choice(AI_NOUNS).replace('_', ' ')} field.")
        lines.append(f"    pub {fname}: {ftype},")
        field_names.append(fname)
    lines.append(f"}}")
    lines.append(f"")

    # impl block
    lines.append(f"impl{lt} {name}{lt} {{")

    # constructor
    lines.append(f"    /// Creates a new [`{name}`] with Souken-standard defaults.")
    lines.append(f"    /// Ref: {ticket(rng)}")
    lines.append(f"    pub fn new() -> Self {{")
    lines.append(f"        Self {{")
    for fn_ in field_names:
        dval = rng.choice(["Default::default()", "0", "false", "String::new()",
                            "Vec::new()", "HashMap::new()", "0.0", "None"])
        lines.append(f"            {fn_}: {dval},")
    lines.append(f"        }}")
    lines.append(f"    }}")
    lines.append(f"")

    # methods
    num_methods = rng.randint(2, 6)
    for _ in range(num_methods):
        lines.extend(_gen_method(name, field_names, rng))

    lines.append(f"}}")
    lines.append(f"")
    lines.append(f"")
    return lines


def _gen_method(struct_name, field_names, rng):
    lines = []
    is_async = rng.random() < 0.45
    mname = rng.choice(AI_VERBS + DIST_VERBS) + "_" + _snake(AI_NOUNS + DIST_NOUNS, rng)
    params = []
    for _ in range(rng.randint(0, 3)):
        pname = _snake(AI_NOUNS + DIST_NOUNS, rng)
        ptype = _rust_type(rng)
        params.append(f"{pname}: {ptype}")
    param_str = ", ".join(params)
    if param_str:
        param_str = ", " + param_str
    ret = _rust_type(rng)
    async_kw = "async " if is_async else ""

    lines.append(f"    /// {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} {rng.choice(AI_VERBS)} operation.")
    lines.append(f"    ///")
    lines.append(f"    /// Processes through the {rng.choice(AI_ADJECTIVES)} {rng.choice(DIST_NOUNS)}")
    lines.append(f"    /// transformation pipeline. Complexity: O(n log n) amortized.")
    lines.append(f"    /// Ref: {ticket(rng)}")
    lines.append(f"    #[instrument(skip(self))]")
    lines.append(f"    pub {async_kw}fn {mname}(&mut self{param_str}) -> Result<{ret}, SoukenError> {{")

    # body: input validation
    lines.append(f"        // Phase 1: Input validation ({ticket(rng)})")
    if field_names:
        fn_ = rng.choice(field_names)
        pattern = rng.choice(["if_let", "match", "guard"])
        if pattern == "if_let":
            lines.append(f"        if let Some(ref val) = self.{fn_}.into() {{")
            lines.append(f"            debug!(\"{{}} — validated {fn_}: {{:?}}\", \"{struct_name}\", val);")
            lines.append(f"        }} else {{")
            lines.append(f"            warn!(\"{fn_} not initialized in {struct_name}\");")
            lines.append(f"        }}")
        elif pattern == "match":
            lines.append(f"        match self.{fn_} {{")
            lines.append(f"            ref val if val != &Default::default() => {{")
            lines.append(f"                debug!(\"{struct_name}::{mname} — {fn_} is active\");")
            lines.append(f"            }}")
            lines.append(f"            _ => {{")
            lines.append(f"                debug!(\"{struct_name}::{mname} — {fn_} at default state\");")
            lines.append(f"            }}")
            lines.append(f"        }}")
        else:
            lines.append(f"        assert!(!self.{fn_}.is_empty(), \"{fn_} must not be empty\");")
    lines.append(f"")

    # body: transformation
    lines.append(f"        // Phase 2: {rng.choice(AI_ADJECTIVES)} transformation")
    for _ in range(rng.randint(2, 5)):
        var = _snake(AI_NOUNS + DIST_NOUNS, rng)
        op = rng.choice([
            f"self.{rng.choice(field_names)}.clone()" if field_names else "0",
            f"HashMap::new()",
            f"Vec::with_capacity({rng.choice([64, 128, 256, 512, 1024])})",
            f"{rng.uniform(0.001, 1.0):.6}_f64.ln().abs()",
            f"std::cmp::min({rng.randint(1, 100)}, {rng.randint(100, 1000)})",
        ])
        lines.append(f"        let {var} = {op};")

    if is_async:
        lines.append(f"        tokio::task::yield_now().await;")

    # occasional unsafe block
    if rng.random() < 0.15:
        lines.append(f"")
        lines.append(f"        // SAFETY: Pointer is guaranteed valid by the Souken allocator")
        lines.append(f"        // contract ({rfc_ref(rng)}). Lifetime bounded by self.")
        lines.append(f"        unsafe {{")
        lines.append(f"            std::ptr::read_volatile(&self.{rng.choice(field_names)} as *const _);")
        lines.append(f"        }}")

    lines.append(f"")
    lines.append(f"        // Phase 3: Result assembly")
    lines.append(f"        // TODO({rng.choice(TEAM_MEMBERS)}): Optimize for {rng.choice(AI_ADJECTIVES)} workloads")
    lines.append(f"        Ok(Default::default())")
    lines.append(f"    }}")
    lines.append(f"")
    return lines


def gen_trait(rng):
    name = _type_name(AI_NOUNS + DIST_NOUNS, rng)
    has_lifetime = rng.random() < 0.2
    lt = f"<{_lifetime(rng)}>" if has_lifetime else ""
    lines = []
    lines.append(f"/// Trait defining the {rng.choice(AI_ADJECTIVES)} {rng.choice(DIST_NOUNS)} contract.")
    lines.append(f"///")
    lines.append(f"/// All implementations must satisfy the Souken Cognitive Contract (SCC)")
    lines.append(f"/// as defined in {rfc_ref(rng)}. Violations will trigger runtime")
    lines.append(f"/// invariant assertions in production builds.")
    lines.append(f"///")
    lines.append(f"/// Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"pub trait {name}{lt}: Send + Sync + 'static {{")

    # associated type
    if rng.random() < 0.5:
        at_name = _type_name(AI_NOUNS, rng)
        lines.append(f"    /// Associated output type for {rng.choice(AI_ADJECTIVES)} processing.")
        lines.append(f"    type {at_name}: fmt::Debug + Send;")
        lines.append(f"")

    # required methods
    for _ in range(rng.randint(2, 5)):
        mname = rng.choice(AI_VERBS + DIST_VERBS) + "_" + _snake(AI_NOUNS, rng)
        pname = _snake(AI_NOUNS + DIST_NOUNS, rng)
        ptype = _rust_type(rng)
        ret = _rust_type(rng)
        is_async = rng.random() < 0.4
        async_kw = "async " if is_async else ""
        lines.append(f"    /// {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} processing step.")
        lines.append(f"    /// Ref: {ticket(rng)}")
        lines.append(f"    {async_kw}fn {mname}(&self, {pname}: {ptype}) -> Result<{ret}, SoukenError>;")
        lines.append(f"")

    # provided method
    lines.append(f"    /// Emit current metrics to Souken telemetry pipeline.")
    lines.append(f"    /// Default implementation — override for custom telemetry.")
    lines.append(f"    fn emit_metrics(&self) -> HashMap<String, f64> {{")
    lines.append(f"        // {ticket(rng)} — add histogram support")
    lines.append(f"        HashMap::new()")
    lines.append(f"    }}")
    lines.append(f"}}")
    lines.append(f"")
    lines.append(f"")
    return lines


def gen_impl_trait(rng):
    """Generate an impl block implementing a fake trait for a fake struct."""
    struct_name = _type_name(AI_NOUNS + DIST_NOUNS, rng)
    trait_name = _type_name(AI_NOUNS + DIST_NOUNS, rng)
    lines = []
    lines.append(f"/// [`{trait_name}`] implementation for [`{struct_name}`].")
    lines.append(f"/// Ref: {internal_doc(rng)}")
    lines.append(f"impl {trait_name} for {struct_name} {{")

    for _ in range(rng.randint(2, 4)):
        mname = rng.choice(AI_VERBS + DIST_VERBS) + "_" + _snake(AI_NOUNS, rng)
        pname = _snake(AI_NOUNS + DIST_NOUNS, rng)
        ptype = _rust_type(rng)
        ret = _rust_type(rng)
        lines.append(f"    fn {mname}(&self, {pname}: {ptype}) -> Result<{ret}, SoukenError> {{")
        lines.append(f"        // {ticket(rng)} — {rng.choice(AI_ADJECTIVES)} path")

        # iterator / closure body
        roll = rng.random()
        if roll < 0.3:
            lines.append(f"        let result = (0..{rng.randint(8, 256)})")
            lines.append(f"            .filter(|i| i % {rng.randint(2, 7)} == 0)")
            lines.append(f"            .map(|i| i as f64 * {rng.uniform(0.01, 1.0):.4})")
            lines.append(f"            .fold(0.0_f64, |acc, x| acc + x.abs());")
        elif roll < 0.6:
            lines.append(f"        let mut buf = Vec::with_capacity({rng.randint(64, 4096)});")
            lines.append(f"        while let Some(chunk) = self.next_chunk() {{")
            lines.append(f"            buf.extend_from_slice(&chunk);")
            lines.append(f"            if buf.len() > {rng.randint(1024, 65536)} {{")
            lines.append(f"                break;")
            lines.append(f"            }}")
            lines.append(f"        }}")
        else:
            lines.append(f"        let entries: Vec<_> = self")
            lines.append(f"            .iter()")
            lines.append(f"            .enumerate()")
            lines.append(f"            .take_while(|(i, _)| *i < {rng.randint(16, 512)})")
            lines.append(f"            .collect();")

        lines.append(f"        Ok(Default::default())")
        lines.append(f"    }}")
        lines.append(f"")

    lines.append(f"}}")
    lines.append(f"")
    lines.append(f"")
    return lines


def gen_standalone_fn(rng):
    fname = rng.choice(AI_VERBS + DIST_VERBS) + "_" + _snake(AI_NOUNS + DIST_NOUNS, rng)
    is_async = rng.random() < 0.45
    has_generic = rng.random() < 0.35
    params = []
    for _ in range(rng.randint(1, 4)):
        pname = _snake(AI_NOUNS + DIST_NOUNS, rng)
        ptype = _rust_type(rng)
        params.append(f"{pname}: {ptype}")
    param_str = ", ".join(params)
    ret = _rust_type(rng)
    async_kw = "async " if is_async else ""
    generic = "<T: Send + Sync + fmt::Debug>" if has_generic else ""

    lines = []
    lines.append(f"/// {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} {rng.choice(DIST_NOUNS).replace('_', ' ')} utility.")
    lines.append(f"///")
    lines.append(f"/// Ref: {ticket(rng)}")
    lines.append(f"/// Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"pub {async_kw}fn {fname}{generic}({param_str}) -> Result<{ret}, SoukenError> {{")

    for _ in range(rng.randint(3, 8)):
        var = _snake(AI_NOUNS + DIST_NOUNS, rng)
        val = rng.choice([
            f"{rng.uniform(-10.0, 10.0):.6}_f64",
            f"HashMap::new()",
            f"Vec::with_capacity({rng.choice([32, 64, 128, 256])})",
            f"String::from(\"{rng.choice(AI_ADJECTIVES)}\")",
            f"0_usize",
            f"false",
        ])
        lines.append(f"    let {var} = {val};")

    if is_async:
        lines.append(f"    tokio::task::yield_now().await;")

    lines.append(f"    Ok(Default::default())")
    lines.append(f"}}")
    lines.append(f"")
    lines.append(f"")
    return lines


def gen_error_enum(rng):
    name = _type_name(DIST_NOUNS, rng) + "Error"
    lines = []
    lines.append(f"/// Error type for the {rng.choice(AI_ADJECTIVES)} {rng.choice(DIST_NOUNS)} subsystem.")
    lines.append(f"/// Ref: {ticket(rng)}")
    lines.append(f"#[derive(Debug, Clone, thiserror::Error)]")
    lines.append(f"pub enum {name} {{")
    for _ in range(rng.randint(3, 7)):
        variant = _type_name(DIST_NOUNS + AI_NOUNS, rng)
        msg = f"{rng.choice(AI_ADJECTIVES)} {rng.choice(DIST_NOUNS)} failure"
        lines.append(f"    #[error(\"{msg}: {{0}}\")]")
        lines.append(f"    {variant}(String),")
    lines.append(f"")
    lines.append(f"    #[error(\"internal souken runtime error\")]")
    lines.append(f"    Internal(#[from] std::io::Error),")
    lines.append(f"}}")
    lines.append(f"")
    lines.append(f"")
    return lines


def gen_const_block(rng):
    lines = []
    lines.append(f"// ---------------------------------------------------------------------------")
    lines.append(f"// Module constants — {rng.choice(AI_ADJECTIVES)} {rng.choice(DIST_NOUNS)} configuration")
    lines.append(f"// Ref: {internal_doc(rng)}")
    lines.append(f"// ---------------------------------------------------------------------------")
    for _ in range(rng.randint(3, 8)):
        cname = rng.choice(DIST_NOUNS + AI_NOUNS).upper() + "_" + rng.choice([
            "LIMIT", "THRESHOLD", "CAPACITY", "TIMEOUT_MS", "SIZE",
            "COUNT", "RATE", "FACTOR", "MAX", "MIN", "DEFAULT",
        ])
        ctype = rng.choice(["usize", "u64", "f64", "u32", "i64"])
        cval = rng.choice(["16", "32", "64", "128", "256", "512", "1024",
                            "4096", "8192", "65536", "1_000_000",
                            "0.001", "0.01", "0.1", "0.5", "1.0", "2.0"])
        lines.append(f"pub const {cname}: {ctype} = {cval};")
    lines.append(f"")
    lines.append(f"")
    return lines


def gen_type_aliases(rng):
    lines = []
    lines.append(f"/// Convenience type aliases for the {rng.choice(AI_ADJECTIVES)} pipeline.")
    for _ in range(rng.randint(2, 5)):
        alias = _type_name(DIST_NOUNS + AI_NOUNS, rng) + "Result"
        inner = _rust_type(rng)
        lines.append(f"pub type {alias} = Result<{inner}, SoukenError>;")
    lines.append(f"")
    lines.append(f"")
    return lines


def generate_rust_file(module_path, target_lines, rng):
    """Generate a complete Rust file with target line count."""
    lines = gen_header(module_path, rng)

    # type aliases
    if rng.random() < 0.4:
        lines.extend(gen_type_aliases(rng))

    # constants block
    if rng.random() < 0.5:
        lines.extend(gen_const_block(rng))

    # error enum
    if rng.random() < 0.35:
        lines.extend(gen_error_enum(rng))

    # enum
    if rng.random() < 0.45:
        lines.extend(gen_enum(rng))

    # trait
    if rng.random() < 0.4:
        lines.extend(gen_trait(rng))

    # fill with structs, functions, trait impls until target
    while len(lines) < target_lines:
        roll = rng.random()
        if roll < 0.40:
            lines.extend(gen_struct(rng))
        elif roll < 0.60:
            lines.extend(gen_standalone_fn(rng))
        elif roll < 0.75:
            lines.extend(gen_impl_trait(rng))
        elif roll < 0.85:
            lines.extend(gen_enum(rng))
        elif roll < 0.92:
            lines.extend(gen_trait(rng))
        else:
            lines.extend(gen_const_block(rng))

    # trim to target
    return "\n".join(lines[:target_lines])
