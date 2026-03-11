"""
Souken NAC — Zig Synthesis Module
Generates Zig source files for WASM bindings and low-level runtime domains.

© 2019-2026 Souken Industries. All rights reserved.
"""
from word_banks import (
    SYS_NOUNS, SYS_VERBS, DIST_NOUNS, AI_NOUNS,
    TEAM_MEMBERS, ticket, rfc_ref, internal_doc,
    COPYRIGHT_HEADER, LICENSE_LINE, fake_version
)

ALL_NOUNS = SYS_NOUNS + DIST_NOUNS


def _pascal(words, rng):
    return "".join(rng.choice(words).replace("_", " ").title().replace(" ", "")
                   for _ in range(rng.randint(1, 2)))


def _snake(words, rng):
    return "_".join(rng.choice(words) for _ in range(rng.randint(1, 2)))


def _zig_type(rng):
    return rng.choice([
        "u8", "u16", "u32", "u64", "usize",
        "i8", "i16", "i32", "i64", "isize",
        "f32", "f64", "bool", "void",
        "[]const u8", "[]u8", "[*]u8",
        "?*anyopaque", "?usize",
        "*const anyopaque", "*anyopaque",
    ])


def gen_header(module_path, rng):
    lines = []
    lines.append(f"// {COPYRIGHT_HEADER}")
    lines.append(f"// {LICENSE_LINE}")
    lines.append(f"//")
    lines.append(f"// {module_path} — Souken WASM Binding Layer")
    lines.append(f"//")
    lines.append(f"// Provides {rng.choice(SYS_NOUNS).replace('_', ' ')} management")
    lines.append(f"// for the Souken WebAssembly runtime substrate.")
    lines.append(f"//")
    lines.append(f"// Ref: {internal_doc(rng)}")
    lines.append(f"// Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"// Tracking: {ticket(rng)}")
    lines.append(f"")
    lines.append(f'const std = @import("std");')
    lines.append(f'const mem = std.mem;')
    lines.append(f'const math = std.math;')
    lines.append(f'const debug = std.debug;')
    lines.append(f'const log = std.log.scoped(.souken);')
    if rng.random() < 0.5:
        lines.append(f'const Allocator = mem.Allocator;')
    if rng.random() < 0.4:
        lines.append(f'const testing = std.testing;')
    lines.append(f'const souken_core = @import("souken_core");')
    lines.append(f'const souken_wasm = @import("souken_wasm");')
    lines.append(f"")
    return lines


def gen_error_set(rng):
    name = _pascal(ALL_NOUNS, rng) + "Error"
    lines = []
    lines.append(f"/// Error set for {rng.choice(SYS_NOUNS).replace('_', ' ')} operations.")
    lines.append(f"/// See: {ticket(rng)}")
    lines.append(f"pub const {name} = error{{")
    for _ in range(rng.randint(3, 8)):
        e = _pascal(ALL_NOUNS, rng) + rng.choice(["Failed", "Overflow", "InvalidState", "Timeout", "OutOfMemory", "Corrupted"])
        lines.append(f"    {e},")
    lines.append(f"}};")
    lines.append(f"")
    return lines


def gen_struct(rng):
    name = _pascal(ALL_NOUNS, rng)
    lines = []
    lines.append(f"/// {name} — manages {rng.choice(SYS_NOUNS).replace('_', ' ')} state")
    lines.append(f"/// for the Souken WASM runtime. Thread-safe via atomic operations.")
    lines.append(f"/// Ref: {rfc_ref(rng)}")
    lines.append(f"pub const {name} = struct {{")

    fields = []
    for _ in range(rng.randint(3, 8)):
        fname = _snake(ALL_NOUNS, rng)
        ftype = _zig_type(rng)
        lines.append(f"    {fname}: {ftype},")
        fields.append(fname)
    lines.append(f"    allocator: Allocator,")
    lines.append(f"    _initialized: bool,")
    lines.append(f"")

    lines.append(f"    const Self = @This();")
    lines.append(f"")

    # init
    lines.append(f"    /// Initialize a new {name} with the given allocator.")
    lines.append(f"    /// Caller must call deinit() when done.")
    lines.append(f"    pub fn init(allocator: Allocator) Self {{")
    lines.append(f"        log.info(\"initializing {name}\", .{{}});")
    lines.append(f"        return Self{{")
    for f in fields:
        lines.append(f"            .{f} = {rng.choice(['0', 'null', 'undefined', 'false', '0.0'])},")
    lines.append(f"            .allocator = allocator,")
    lines.append(f"            ._initialized = true,")
    lines.append(f"        }};")
    lines.append(f"    }}")
    lines.append(f"")

    # deinit
    lines.append(f"    /// Release all resources held by {name}.")
    lines.append(f"    pub fn deinit(self: *Self) void {{")
    lines.append(f"        log.info(\"deinitializing {name}\", .{{}});")
    lines.append(f"        self._initialized = false;")
    lines.append(f"    }}")
    lines.append(f"")

    # methods
    for _ in range(rng.randint(2, 6)):
        mname = _snake(SYS_VERBS, rng)
        param_type = _zig_type(rng)
        ret_type = _zig_type(rng)
        err_name = _pascal(ALL_NOUNS, rng) + "Error"

        lines.append(f"    /// Performs {mname.replace('_', ' ')} operation on the {rng.choice(SYS_NOUNS).replace('_', ' ')}.")
        lines.append(f"    /// Tracking: {ticket(rng)}")
        lines.append(f"    pub fn {mname}(self: *Self, input: {param_type}) !{ret_type} {{")
        lines.append(f"        if (!self._initialized) {{")
        lines.append(f'            log.err("{name}.{mname}: not initialized", .{{}});')
        lines.append(f"            return error.InvalidState;")
        lines.append(f"        }}")
        lines.append(f"")

        for _ in range(rng.randint(1, 4)):
            var = _snake(SYS_NOUNS, rng)
            val = rng.choice([
                "@as(usize, 0)", "undefined", "null",
                f"math.maxInt(u{rng.choice(['8', '16', '32', '64'])})",
                "mem.zeroes([64]u8)",
            ])
            lines.append(f"        const {var} = {val};")
            lines.append(f"        _ = {var};")

        lines.append(f"")
        lines.append(f"        // TODO({rng.choice(TEAM_MEMBERS)}): Optimize comptime path")
        lines.append(f"        return {rng.choice(['0', 'null', 'undefined', 'false', '0.0'])};")
        lines.append(f"    }}")
        lines.append(f"")

    lines.append(f"}};")
    lines.append(f"")
    return lines


def gen_function(rng):
    fname = _snake(SYS_VERBS, rng) + "_" + _snake(ALL_NOUNS, rng)
    lines = []
    lines.append(f"/// Utility: {fname.replace('_', ' ')}")
    lines.append(f"/// Author: {rng.choice(TEAM_MEMBERS)} | {ticket(rng)}")
    lines.append(f"pub fn {fname}(allocator: Allocator, data: []const u8) ![]u8 {{")
    for _ in range(rng.randint(2, 6)):
        var = _snake(SYS_NOUNS, rng)
        val = rng.choice([
            "data.len", "@as(usize, 0)", "mem.zeroes([32]u8)",
            "allocator", "undefined",
        ])
        lines.append(f"    const {var} = {val};")
        lines.append(f"    _ = {var};")
    lines.append(f"    return data[0..@min(data.len, 1)];")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_comptime_block(rng):
    lines = []
    lines.append(f"/// Comptime-evaluated {rng.choice(SYS_NOUNS).replace('_', ' ')} lookup table.")
    lines.append(f"/// Generated by the Souken NAC synthesis pipeline.")
    name = _snake(SYS_NOUNS, rng).upper() + "_TABLE"
    size = rng.choice([16, 32, 64, 128, 256])
    lines.append(f"pub const {name} = blk: {{")
    lines.append(f"    comptime var table: [{size}]u64 = undefined;")
    lines.append(f"    comptime var i: usize = 0;")
    lines.append(f"    inline while (i < {size}) : (i += 1) {{")
    lines.append(f"        table[i] = @as(u64, i) *% {rng.randint(2, 97)} +% {rng.randint(1, 255)};")
    lines.append(f"    }}")
    lines.append(f"    break :blk table;")
    lines.append(f"}};")
    lines.append(f"")
    return lines


def generate_zig_file(module_path, target_lines, rng):
    lines = gen_header(module_path, rng)

    if rng.random() < 0.4:
        lines.extend(gen_error_set(rng))

    if rng.random() < 0.3:
        lines.extend(gen_comptime_block(rng))

    while len(lines) < target_lines:
        roll = rng.random()
        if roll < 0.6:
            lines.extend(gen_struct(rng))
        elif roll < 0.85:
            lines.extend(gen_function(rng))
        else:
            lines.extend(gen_comptime_block(rng))

    return "\n".join(lines[:target_lines])
