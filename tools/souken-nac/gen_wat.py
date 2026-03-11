"""
Souken NAC — WAT (WebAssembly Text) Synthesis Module
Generates WAT files for the Souken WASM runtime.

© 2019-2026 Souken Industries. All rights reserved.
"""
from word_banks import (
    SYS_NOUNS, SYS_VERBS, AI_NOUNS,
    TEAM_MEMBERS, ticket, internal_doc,
    COPYRIGHT_HEADER, LICENSE_LINE
)

ALL_NOUNS = SYS_NOUNS + AI_NOUNS


def _snake(words, rng):
    return "_".join(rng.choice(words) for _ in range(rng.randint(1, 2)))


def _wat_type(rng):
    return rng.choice(["i32", "i64", "f32", "f64"])


def gen_header(module_path, rng):
    lines = []
    lines.append(f";; {COPYRIGHT_HEADER}")
    lines.append(f";; {LICENSE_LINE}")
    lines.append(f";;")
    lines.append(f";; {module_path} — Souken WASM Runtime Module")
    lines.append(f";; Implements {rng.choice(SYS_NOUNS).replace('_', ' ')} operations")
    lines.append(f";; for the Souken WebAssembly execution substrate.")
    lines.append(f";;")
    lines.append(f";; Ref: {internal_doc(rng)}")
    lines.append(f";; Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f";; Tracking: {ticket(rng)}")
    lines.append(f"")
    lines.append(f"(module")
    lines.append(f"")

    # memory and table declarations
    lines.append(f"  ;; Memory: {rng.randint(1, 16)} pages ({rng.randint(1, 16) * 64}KB)")
    lines.append(f"  (memory (export \"memory\") {rng.randint(1, 16)})")
    lines.append(f"")
    lines.append(f"  ;; Global state for {rng.choice(SYS_NOUNS).replace('_', ' ')} tracking")
    for _ in range(rng.randint(2, 5)):
        gname = "$g_" + _snake(SYS_NOUNS, rng)
        gtype = _wat_type(rng)
        lines.append(f"  (global {gname} (mut {gtype}) ({gtype}.const 0))")
    lines.append(f"")
    return lines


def gen_function(rng):
    fname = "$" + _snake(SYS_VERBS, rng) + "_" + _snake(ALL_NOUNS, rng)
    lines = []
    lines.append(f"  ;; {fname}: {rng.choice(SYS_VERBS).replace('_', ' ')} the {rng.choice(SYS_NOUNS).replace('_', ' ')}")
    lines.append(f"  ;; Tracking: {ticket(rng)}")

    num_params = rng.randint(1, 4)
    num_locals = rng.randint(1, 4)
    result_type = _wat_type(rng)

    param_str = " ".join(f"(param ${_snake(SYS_NOUNS, rng)} {_wat_type(rng)})" for _ in range(num_params))
    lines.append(f"  (func {fname} (export \"{fname[1:]}\") {param_str} (result {result_type})")

    for _ in range(num_locals):
        lname = "$l_" + _snake(SYS_NOUNS, rng)
        ltype = _wat_type(rng)
        lines.append(f"    (local {lname} {ltype})")

    lines.append(f"")
    lines.append(f"    ;; Phase 1: Validate inputs")

    # body with WAT instructions
    for _ in range(rng.randint(3, 10)):
        op = rng.choice([
            f"    ({result_type}.const {rng.randint(0, 65535)})",
            f"    ({result_type}.add)",
            f"    ({result_type}.sub)",
            f"    ({result_type}.mul)",
            f"    (drop)",
            f"    ({result_type}.const {rng.randint(0, 255)})",
            f"    ({result_type}.load offset={rng.randint(0, 1024)})",
            f"    ({result_type}.store offset={rng.randint(0, 1024)})",
            f"    ;; {rng.choice(SYS_NOUNS).replace('_', ' ')} checkpoint",
            f"    (nop)  ;; alignment padding for {rng.choice(SYS_NOUNS).replace('_', ' ')}",
        ])
        lines.append(op)

    lines.append(f"")
    lines.append(f"    ;; Return result")
    lines.append(f"    ({result_type}.const 0)")
    lines.append(f"  )")
    lines.append(f"")
    return lines


def gen_table(rng):
    lines = []
    size = rng.randint(4, 16)
    lines.append(f"  ;; Function table for indirect {rng.choice(SYS_NOUNS).replace('_', ' ')} dispatch")
    lines.append(f"  ;; See: {ticket(rng)}")
    lines.append(f"  (table {size} funcref)")
    lines.append(f"")
    return lines


def gen_data_segment(rng):
    lines = []
    offset = rng.randint(0, 65536)
    data_str = rng.choice([
        "Souken WASM Runtime v" + str(rng.randint(1, 9)) + "." + str(rng.randint(0, 99)),
        "SOUKEN_MAGIC_" + str(rng.randint(1000, 9999)),
        rng.choice(SYS_NOUNS).replace("_", "-") + "-initialized",
        "nexus-wasm-" + str(rng.randint(100, 999)),
    ])
    lines.append(f'  ;; Data segment: {rng.choice(SYS_NOUNS).replace("_", " ")} metadata')
    lines.append(f'  (data (i32.const {offset}) "{data_str}")')
    lines.append(f"")
    return lines


def generate_wat_file(module_path, target_lines, rng):
    lines = gen_header(module_path, rng)

    if rng.random() < 0.5:
        lines.extend(gen_table(rng))

    for _ in range(rng.randint(1, 3)):
        lines.extend(gen_data_segment(rng))

    while len(lines) < target_lines - 2:
        lines.extend(gen_function(rng))

    # close module
    lines.append(f")")
    lines.append(f"")

    return "\n".join(lines[:target_lines])
