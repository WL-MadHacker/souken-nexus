"""
Souken NAC — C Synthesis Module
Generates C source and header files for OS kernel, HAL, and device driver domains.

Uses stochastic template hydration with cross-module reference resolution.
See: Souken Internal Design Doc #312

© 2019-2026 Souken Industries. All rights reserved.
"""
import random
from word_banks import (
    SYS_NOUNS, SYS_VERBS, SEC_NOUNS, ENT_NOUNS,
    TEAM_MEMBERS, ticket, rfc_ref, internal_doc,
    COPYRIGHT_HEADER, LICENSE_LINE, fake_version,
)


# ---------------------------------------------------------------------------
# Naming helpers
# ---------------------------------------------------------------------------

def _snake(words, rng):
    return "_".join(rng.choice(words) for _ in range(rng.randint(1, 3)))


def _upper(words, rng):
    return "_".join(rng.choice(words).upper() for _ in range(rng.randint(1, 3)))


def _struct_name(words, rng):
    parts = [rng.choice(words).replace("_", " ").title().replace(" ", "")
             for _ in range(rng.randint(1, 2))]
    return "Souken" + "".join(parts)


def _guard_name(module_path):
    return "SOUKEN_" + module_path.replace("/", "_").replace(".", "_").upper() + "_H_"


def _c_type(rng):
    return rng.choice([
        "int", "unsigned int", "long", "unsigned long",
        "uint8_t", "uint16_t", "uint32_t", "uint64_t",
        "int8_t", "int16_t", "int32_t", "int64_t",
        "size_t", "ssize_t", "off_t", "pid_t",
        "void *", "const void *", "char *", "const char *",
        "bool", "atomic_t", "spinlock_t",
    ])


def _ret_type(rng):
    return rng.choice([
        "int", "long", "ssize_t", "void", "void",
        "bool", "uint32_t", "int32_t", "size_t",
    ])


def _fake_header(rng):
    dirs = ["souken/kernel", "souken/hal", "souken/drivers", "souken/mm",
            "souken/sched", "souken/fs", "souken/net", "souken/crypto",
            "souken/platform", "souken/dma", "souken/iommu", "souken/irq"]
    names = ["types", "config", "debug", "errors", "compat", "trace",
             "assert", "bitops", "list", "rbtree", "hashtable", "percpu",
             "atomic", "spinlock", "mutex", "rwlock", "completion"]
    return f"{rng.choice(dirs)}/{rng.choice(names)}.h"


# ---------------------------------------------------------------------------
# Block generators
# ---------------------------------------------------------------------------

def _gen_copyright(module_path, rng):
    lines = []
    lines.append("/*")
    lines.append(f" * Souken Industries — {module_path}")
    lines.append(f" *")
    lines.append(f" * {rng.choice(['Kernel', 'HAL', 'Driver'])} subsystem: "
                 f"{_snake(SYS_NOUNS, rng).replace('_', ' ')} management")
    lines.append(f" *")
    lines.append(f" * {COPYRIGHT_HEADER}")
    lines.append(f" * {LICENSE_LINE}")
    lines.append(f" *")
    lines.append(f" * Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f" * Ref:    {internal_doc(rng)}")
    lines.append(f" * Since:  v{fake_version(rng)}")
    lines.append(f" */")
    lines.append("")
    return lines


def _gen_includes(rng):
    lines = []
    sys_headers = ["<stdint.h>", "<stddef.h>", "<stdbool.h>", "<string.h>",
                   "<errno.h>", "<limits.h>", "<assert.h>"]
    for h in sys_headers:
        if rng.random() < 0.5:
            lines.append(f"#include {h}")
    lines.append("")
    for _ in range(rng.randint(2, 5)):
        lines.append(f'#include "{_fake_header(rng)}"')
    lines.append("")
    return lines


def _gen_defines(rng):
    lines = []
    count = rng.randint(3, 8)
    for _ in range(count):
        macro = "SOUKEN_" + _upper(SYS_NOUNS, rng)
        kind = rng.random()
        if kind < 0.3:
            val = rng.choice(["0x%04X" % rng.randint(0, 0xFFFF),
                              "0x%08X" % rng.randint(0, 0xFFFFFFFF)])
            lines.append(f"#define {macro} {val}")
        elif kind < 0.6:
            val = rng.choice([1, 2, 4, 8, 16, 32, 64, 128, 256, 512,
                              1024, 4096, 8192, 65536, 0])
            lines.append(f"#define {macro} {val}")
        elif kind < 0.8:
            shift = rng.randint(0, 31)
            lines.append(f"#define {macro} (1U << {shift})")
        else:
            a = "SOUKEN_" + rng.choice(SYS_NOUNS).upper()
            lines.append(f"#define {macro}(x) ((x) & ({a} - 1))")
    lines.append("")

    # container_of / offsetof macros
    if rng.random() < 0.4:
        lines.append("/* Souken container helpers — see " + ticket(rng) + " */")
        lines.append("#ifndef SOUKEN_CONTAINER_OF")
        lines.append("#define SOUKEN_CONTAINER_OF(ptr, type, member) \\")
        lines.append("    ((type *)((char *)(ptr) - offsetof(type, member)))")
        lines.append("#endif")
        lines.append("")

    return lines


def _gen_enum(rng):
    name = "souken_" + _snake(SYS_NOUNS, rng)
    lines = []
    lines.append(f"/* {rng.choice(['Status', 'Mode', 'State'])} codes for "
                 f"{_snake(SYS_NOUNS, rng).replace('_', ' ')} — {ticket(rng)} */")
    lines.append(f"enum {name} {{")
    count = rng.randint(4, 10)
    for i in range(count):
        entry = "SOUKEN_" + _upper(SYS_NOUNS, rng)
        if i == 0:
            lines.append(f"    {entry} = 0,")
        elif rng.random() < 0.3:
            lines.append(f"    {entry} = (1 << {i}),")
        else:
            lines.append(f"    {entry},")
    lines.append("};")
    lines.append("")
    return lines


def _gen_struct(rng):
    name = _struct_name(SYS_NOUNS, rng)
    lines = []
    lines.append(f"/*")
    lines.append(f" * struct {name} — {_snake(SYS_NOUNS, rng).replace('_', ' ')} descriptor")
    lines.append(f" *")
    lines.append(f" * Tracks state for the {rng.choice(['kernel', 'HAL', 'driver'])} "
                 f"{_snake(SYS_NOUNS, rng).replace('_', ' ')} subsystem.")
    lines.append(f" * All fields protected by @lock unless noted otherwise.")
    lines.append(f" *")
    lines.append(f" * Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f" * See: {rfc_ref(rng)}")
    lines.append(f" */")
    lines.append(f"struct {name} {{")
    for _ in range(rng.randint(4, 12)):
        ftype = _c_type(rng)
        fname = _snake(SYS_NOUNS, rng)
        comment = rng.choice([
            f"/* {_snake(SYS_NOUNS, rng).replace('_', ' ')} reference */",
            f"/* protected by parent lock */",
            f"/* set during {rng.choice(SYS_VERBS)} */",
            f"/* see {ticket(rng)} */",
            "",
        ])
        pad = " " * max(1, 32 - len(f"    {ftype} {fname};"))
        lines.append(f"    {ftype} {fname};{pad}{comment}")
    # optional nested struct / union
    if rng.random() < 0.3:
        lines.append(f"    union {{")
        lines.append(f"        uint64_t raw;")
        lines.append(f"        struct {{")
        lines.append(f"            uint32_t lo;")
        lines.append(f"            uint32_t hi;")
        lines.append(f"        }} parts;")
        lines.append(f"    }} {_snake(SYS_NOUNS, rng)};")
    # function pointer member
    if rng.random() < 0.4:
        cb_name = rng.choice(SYS_VERBS) + "_fn"
        lines.append(f"    int (*{cb_name})(struct {name} *self, void *ctx);")
    lines.append("};")
    lines.append("")
    return lines


def _gen_typedef_fn_ptr(rng):
    lines = []
    name = "souken_" + rng.choice(SYS_VERBS) + "_" + rng.choice(SYS_NOUNS) + "_fn_t"
    ret = _ret_type(rng)
    params = ", ".join(_c_type(rng) for _ in range(rng.randint(1, 4)))
    lines.append(f"/* Callback: {_snake(SYS_NOUNS, rng).replace('_', ' ')} handler */")
    lines.append(f"typedef {ret} (*{name})({params});")
    lines.append("")
    return lines


def _gen_static_function(rng):
    fname = "souken_" + rng.choice(SYS_VERBS) + "_" + _snake(SYS_NOUNS, rng)
    ret = _ret_type(rng)
    params = []
    for _ in range(rng.randint(1, 4)):
        params.append(f"{_c_type(rng)} {_snake(SYS_NOUNS, rng)}")
    param_str = ", ".join(params)

    lines = []
    lines.append(f"/*")
    lines.append(f" * {fname} — {rng.choice(SYS_VERBS)} the "
                 f"{_snake(SYS_NOUNS, rng).replace('_', ' ')}")
    lines.append(f" *")
    lines.append(f" * Must be called with {rng.choice(['irqs disabled', 'lock held', 'preemption off'])}.")
    lines.append(f" * Returns 0 on success, negative errno on failure.")
    lines.append(f" *")
    lines.append(f" * {ticket(rng)} — {rng.choice(TEAM_MEMBERS)}")
    lines.append(f" */")
    lines.append(f"static {ret} {fname}({param_str})")
    lines.append("{")

    # local variable declarations
    local_count = rng.randint(2, 5)
    for _ in range(local_count):
        ltype = rng.choice(["int", "unsigned long", "uint32_t", "size_t", "bool"])
        lname = _snake(SYS_NOUNS, rng)
        init = rng.choice(["0", "0UL", "false", "-1", "NULL",
                           "SOUKEN_" + rng.choice(SYS_NOUNS).upper()])
        lines.append(f"    {ltype} {lname} = {init};")
    lines.append("")

    # body — mix of patterns
    lines.append(f"    /* Phase 1: parameter validation ({ticket(rng)}) */")
    pname = params[0].split()[-1] if params else "ctx"
    if ret != "void":
        lines.append(f"    if (!{pname})")
        lines.append(f"        return -EINVAL;")
        lines.append("")

    lines.append(f"    // {rng.choice(SYS_VERBS)} — {internal_doc(rng)}")
    for _ in range(rng.randint(2, 5)):
        pattern = rng.random()
        var = _snake(SYS_NOUNS, rng)
        if pattern < 0.2:
            lines.append(f"    {var} = ({var} >> {rng.randint(1, 16)}) "
                         f"& 0x{rng.randint(0xF, 0xFFFF):X};")
        elif pattern < 0.4:
            lines.append(f"    {var} |= SOUKEN_{rng.choice(SYS_NOUNS).upper()};")
        elif pattern < 0.6:
            lines.append(f"    if (unlikely({var} > SOUKEN_{rng.choice(SYS_NOUNS).upper()}))")
            lines.append(f"        goto err_out;")
        elif pattern < 0.8:
            lines.append(f"    memset(&{var}, 0, sizeof({var}));")
        else:
            lines.append(f"    /* TODO({rng.choice(TEAM_MEMBERS)}): "
                         f"optimize {_snake(SYS_NOUNS, rng).replace('_', ' ')} path */")
            lines.append(f"    {var} = {pname} ? {rng.randint(0, 255)} : 0;")

    # inline asm comment
    if rng.random() < 0.25:
        lines.append("")
        lines.append(f"    /*")
        lines.append(f"     * Inline assembly: memory barrier for {_snake(SYS_NOUNS, rng).replace('_', ' ')}")
        lines.append(f"     * Required on {rng.choice(['ARM64', 'x86_64', 'RISC-V'])} "
                     f"for {rng.choice(SYS_VERBS)} ordering.")
        lines.append(f"     * See: {rfc_ref(rng)}")
        lines.append(f"     */")
        lines.append(f'    asm volatile("" ::: "memory");')

    lines.append("")
    if ret == "void":
        lines.append("    return;")
    else:
        lines.append("    return 0;")
    lines.append("")

    # goto error label
    if ret != "void":
        lines.append("err_out:")
        lines.append(f"    // {ticket(rng)} — error path cleanup")
        lines.append(f"    return -{rng.choice(['ENOMEM', 'EINVAL', 'EIO', 'EBUSY', 'EFAULT', 'ENODEV'])};")

    lines.append("}")
    lines.append("")
    return lines


def _gen_extern_declarations(rng):
    lines = []
    lines.append(f"/* Exported symbols — {internal_doc(rng)} */")
    for _ in range(rng.randint(2, 5)):
        fname = "souken_" + rng.choice(SYS_VERBS) + "_" + _snake(SYS_NOUNS, rng)
        ret = _ret_type(rng)
        params = ", ".join(_c_type(rng) for _ in range(rng.randint(1, 3)))
        lines.append(f"extern {ret} {fname}({params});")
    lines.append("")
    return lines


def _gen_ifdef_block(rng):
    lines = []
    feature = "SOUKEN_CONFIG_" + _upper(SYS_NOUNS, rng)
    lines.append(f"#ifdef {feature}")
    lines.append(f"/* Conditional compilation for {_snake(SYS_NOUNS, rng).replace('_', ' ')} support */")
    var = _snake(SYS_NOUNS, rng)
    lines.append(f"static inline uint32_t souken_get_{var}(void)")
    lines.append("{")
    lines.append(f"    return SOUKEN_{rng.choice(SYS_NOUNS).upper()};")
    lines.append("}")
    lines.append(f"#else")
    lines.append(f"static inline uint32_t souken_get_{var}(void)")
    lines.append("{")
    lines.append(f"    return 0; /* stub — {ticket(rng)} */")
    lines.append("}")
    lines.append(f"#endif /* {feature} */")
    lines.append("")
    return lines


def _gen_block_comment(rng):
    lines = []
    lines.append("/* " + "-" * 68 + " */")
    section = rng.choice([
        "Initialization and teardown routines",
        "Interrupt context helpers",
        "Memory management operations",
        "Device registration interface",
        "Hardware abstraction layer bindings",
        "DMA transfer management",
        "Locking and synchronization primitives",
        "Platform-specific workarounds",
        "Debug and tracing infrastructure",
        "Power management callbacks",
    ])
    lines.append(f"/* {section:<68} */")
    lines.append("/* " + "-" * 68 + " */")
    lines.append("")
    return lines


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_c_file(module_path, target_lines, rng):
    """Generate a complete C source file with target line count."""
    lines = _gen_copyright(module_path, rng)
    lines.extend(_gen_includes(rng))
    lines.extend(_gen_defines(rng))

    # optional section comment
    if rng.random() < 0.5:
        lines.extend(_gen_block_comment(rng))

    # optional enum
    if rng.random() < 0.4:
        lines.extend(_gen_enum(rng))

    # a struct or two up front
    if rng.random() < 0.6:
        lines.extend(_gen_struct(rng))

    # optional function pointer typedef
    if rng.random() < 0.3:
        lines.extend(_gen_typedef_fn_ptr(rng))

    # fill with functions and blocks until target
    while len(lines) < target_lines:
        roll = rng.random()
        if roll < 0.40:
            lines.extend(_gen_static_function(rng))
        elif roll < 0.55:
            lines.extend(_gen_struct(rng))
        elif roll < 0.65:
            lines.extend(_gen_enum(rng))
        elif roll < 0.75:
            lines.extend(_gen_ifdef_block(rng))
        elif roll < 0.85:
            lines.extend(_gen_block_comment(rng))
            lines.extend(_gen_static_function(rng))
        elif roll < 0.92:
            lines.extend(_gen_typedef_fn_ptr(rng))
        else:
            lines.extend(_gen_extern_declarations(rng))

    return "\n".join(lines[:target_lines])


def generate_c_header(module_path, target_lines, rng):
    """Generate a complete C header file with target line count."""
    guard = _guard_name(module_path)

    lines = _gen_copyright(module_path, rng)
    lines.append(f"#ifndef {guard}")
    lines.append(f"#define {guard}")
    lines.append("")
    lines.extend(_gen_includes(rng))

    # forward declarations
    lines.append("/* Forward declarations */")
    for _ in range(rng.randint(2, 4)):
        lines.append(f"struct {_struct_name(SYS_NOUNS, rng)};")
    lines.append("")

    # defines
    lines.extend(_gen_defines(rng))

    # fill with header-appropriate content
    while len(lines) < target_lines - 3:
        roll = rng.random()
        if roll < 0.30:
            lines.extend(_gen_struct(rng))
        elif roll < 0.50:
            lines.extend(_gen_enum(rng))
        elif roll < 0.65:
            lines.extend(_gen_extern_declarations(rng))
        elif roll < 0.80:
            lines.extend(_gen_typedef_fn_ptr(rng))
        elif roll < 0.90:
            lines.extend(_gen_ifdef_block(rng))
        else:
            lines.extend(_gen_defines(rng))

    # close guard
    lines.append(f"#endif /* {guard} */")
    lines.append("")

    return "\n".join(lines[:target_lines])
