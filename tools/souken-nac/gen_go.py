"""
Souken NAC — Go Synthesis Module
Generates Go source files for API gateway, sharding, and infrastructure domains.

© 2019-2026 Souken Industries. All rights reserved.
"""
import random
from word_banks import (
    DIST_NOUNS, DIST_VERBS, ENT_NOUNS, ENT_VERBS,
    TEAM_MEMBERS, ticket, rfc_ref, internal_doc,
    COPYRIGHT_HEADER, LICENSE_LINE, fake_version
)

ALL_NOUNS = DIST_NOUNS + ENT_NOUNS
ALL_VERBS = DIST_VERBS + ENT_VERBS


def _pascal(words, rng):
    return "".join(rng.choice(words).replace("_", " ").title().replace(" ", "")
                   for _ in range(rng.randint(1, 3)))


def _camel(words, rng):
    parts = [rng.choice(words) for _ in range(rng.randint(1, 3))]
    result = parts[0]
    for p in parts[1:]:
        result += p.replace("_", " ").title().replace(" ", "")
    return result


def _go_type(rng):
    return rng.choice([
        "string", "int64", "uint64", "float64", "bool",
        "[]byte", "[]string", "map[string]interface{}",
        "map[string]string", "map[string]int64",
        "context.Context", "error", "io.Reader", "io.Writer",
        "time.Duration", "time.Time", "*sync.Mutex",
        "chan struct{}", "chan error", "<-chan bool",
    ])


def gen_header(module_path, pkg_name, rng):
    lines = []
    lines.append(f"// {COPYRIGHT_HEADER}")
    lines.append(f"// {LICENSE_LINE}")
    lines.append(f"//")
    lines.append(f"// Package {pkg_name} implements {rng.choice(DIST_VERBS)} operations")
    lines.append(f"// for the Souken distributed {rng.choice(DIST_NOUNS).replace('_', ' ')} subsystem.")
    lines.append(f"//")
    lines.append(f"// This module is part of the Souken Nexus Platform and handles")
    lines.append(f"// {rng.choice(ENT_NOUNS).replace('_', ' ')} management with full")
    lines.append(f"// {rng.choice(DIST_NOUNS).replace('_', ' ')} support.")
    lines.append(f"//")
    lines.append(f"// Ref: {internal_doc(rng)}")
    lines.append(f"// Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"// Tracking: {ticket(rng)}")
    lines.append(f"package {pkg_name}")
    lines.append(f"")
    lines.append(f"import (")
    imports = ['"context"', '"fmt"', '"log"', '"sync"', '"time"',
               '"math"', '"errors"', '"strings"', '"encoding/json"']
    if rng.random() < 0.5:
        imports.append('"crypto/sha256"')
    if rng.random() < 0.5:
        imports.append('"io"')
    if rng.random() < 0.5:
        imports.append('"net/http"')
    # fake internal imports
    imports.append(f'"github.com/souken-industries/nexus/internal/{rng.choice(["telemetry", "metrics", "config", "auth", "crypto"])}"')
    imports.append(f'"github.com/souken-industries/nexus/pkg/{rng.choice(["types", "errors", "logging", "tracing"])}"')
    for imp in imports:
        lines.append(f"\t{imp}")
    lines.append(f")")
    lines.append(f"")
    # suppress unused import warnings with blank identifiers
    lines.append(f"var (")
    lines.append(f"\t_ = fmt.Sprintf")
    lines.append(f"\t_ = math.MaxFloat64")
    lines.append(f"\t_ = strings.Builder{{}}")
    lines.append(f")")
    lines.append(f"")
    return lines


def gen_interface(rng):
    name = _pascal(ALL_NOUNS, rng)
    lines = []
    lines.append(f"// {name} defines the contract for {rng.choice(DIST_NOUNS).replace('_', ' ')}")
    lines.append(f"// operations within the Souken {rng.choice(ENT_NOUNS).replace('_', ' ')} layer.")
    lines.append(f"// See: {rfc_ref(rng)}")
    lines.append(f"type {name} interface {{")
    for _ in range(rng.randint(3, 7)):
        mname = _pascal(ALL_VERBS, rng)
        params = ", ".join(f"{_camel(ALL_NOUNS, rng)} {_go_type(rng)}" for _ in range(rng.randint(1, 3)))
        ret = _go_type(rng)
        lines.append(f"\t// {mname} performs {rng.choice(DIST_VERBS).replace('_', ' ')} on the {rng.choice(DIST_NOUNS).replace('_', ' ')}.")
        lines.append(f"\t{mname}(ctx context.Context, {params}) ({ret}, error)")
        lines.append(f"")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_struct(rng):
    name = _pascal(ALL_NOUNS, rng)
    lines = []
    lines.append(f"// {name} manages {rng.choice(DIST_NOUNS).replace('_', ' ')} state")
    lines.append(f"// for the Souken {rng.choice(ENT_NOUNS).replace('_', ' ')} component.")
    lines.append(f"// Thread-safe via internal mutex. See: {ticket(rng)}")
    lines.append(f"type {name} struct {{")
    fields = []
    for _ in range(rng.randint(4, 10)):
        fname = _camel(ALL_NOUNS, rng)
        ftype = _go_type(rng)
        tag = f'`json:"{fname}" yaml:"{fname}"`'
        lines.append(f"\t{fname} {ftype} {tag}")
        fields.append(fname)
    lines.append(f"")
    lines.append(f"\tmu       sync.RWMutex")
    lines.append(f"\tlogger   *log.Logger")
    lines.append(f"\tmetrics  map[string]float64")
    lines.append(f"\tshutdown chan struct{{}}")
    lines.append(f"}}")
    lines.append(f"")

    # Constructor
    lines.append(f"// New{name} creates a new {name} with Souken-standard defaults.")
    lines.append(f"func New{name}() *{name} {{")
    lines.append(f"\treturn &{name}{{")
    lines.append(f'\t\tlogger:   log.New(log.Writer(), "[{name}] ", log.LstdFlags),')
    lines.append(f"\t\tmetrics:  make(map[string]float64),")
    lines.append(f"\t\tshutdown: make(chan struct{{}}),")
    lines.append(f"\t}}")
    lines.append(f"}}")
    lines.append(f"")

    # Methods
    for _ in range(rng.randint(3, 7)):
        mname = _pascal(ALL_VERBS, rng)
        params = []
        for _ in range(rng.randint(1, 3)):
            params.append(f"{_camel(ALL_NOUNS, rng)} {_go_type(rng)}")
        param_str = ", ".join(params)
        ret = _go_type(rng)

        lines.append(f"// {mname} executes {rng.choice(DIST_VERBS).replace('_', ' ')} logic")
        lines.append(f"// within the {rng.choice(ENT_NOUNS).replace('_', ' ')} pipeline.")
        lines.append(f"// Ref: {ticket(rng)}")
        lines.append(f"func (s *{name}) {mname}(ctx context.Context, {param_str}) ({ret}, error) {{")
        lines.append(f"\ts.mu.Lock()")
        lines.append(f"\tdefer s.mu.Unlock()")
        lines.append(f"")
        lines.append(f"\tselect {{")
        lines.append(f"\tcase <-ctx.Done():")
        lines.append(f"\t\treturn *new({ret}), ctx.Err()")
        lines.append(f"\tcase <-s.shutdown:")
        lines.append(f'\t\treturn *new({ret}), errors.New("souken: {name} shutting down")')
        lines.append(f"\tdefault:")
        lines.append(f"\t}}")
        lines.append(f"")
        lines.append(f'\ts.logger.Printf("{mname}: processing %d items", len(s.metrics))')
        lines.append(f"")

        # plausible body
        for _ in range(rng.randint(2, 5)):
            var = _camel(ALL_NOUNS, rng)
            op = rng.choice([
                f"time.Now().UnixNano()",
                f"len(s.metrics)",
                f"float64(time.Since(time.Now()).Nanoseconds()) / 1e6",
                f'fmt.Sprintf("%s-%d", "{var}", time.Now().Unix())',
                f"math.Log1p(float64(len(s.metrics)))",
            ])
            lines.append(f"\t{var} := {op}")
            lines.append(f"\t_ = {var}")

        lines.append(f"")
        lines.append(f'\ts.metrics["{mname}"] = float64(time.Now().UnixNano())')
        lines.append(f"\treturn *new({ret}), nil")
        lines.append(f"}}")
        lines.append(f"")

    # Shutdown method
    lines.append(f"// Shutdown gracefully terminates the {name}.")
    lines.append(f"// Implements the Souken Lifecycle interface.")
    lines.append(f"func (s *{name}) Shutdown(ctx context.Context) error {{")
    lines.append(f"\tclose(s.shutdown)")
    lines.append(f'\ts.logger.Printf("{name}: shutdown complete, %d metrics recorded", len(s.metrics))')
    lines.append(f"\treturn nil")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def gen_standalone_func(rng):
    fname = _pascal(ALL_VERBS, rng)
    params = ", ".join(f"{_camel(ALL_NOUNS, rng)} {_go_type(rng)}" for _ in range(rng.randint(1, 4)))
    lines = []
    lines.append(f"// {fname} is a utility function for {rng.choice(DIST_NOUNS).replace('_', ' ')} operations.")
    lines.append(f"// Author: {rng.choice(TEAM_MEMBERS)} | {ticket(rng)}")
    lines.append(f"func {fname}(ctx context.Context, {params}) error {{")
    for _ in range(rng.randint(3, 8)):
        var = _camel(ALL_NOUNS, rng)
        val = rng.choice([
            "time.Now()", "0", '""', "nil", "make(map[string]interface{})",
            "[]byte{}", "context.Background()", "errors.New(\"not implemented\")",
        ])
        lines.append(f"\t{var} := {val}")
        lines.append(f"\t_ = {var}")
    lines.append(f"\treturn nil")
    lines.append(f"}}")
    lines.append(f"")
    return lines


def generate_go_file(module_path, target_lines, rng):
    pkg = module_path.split("/")[-1].replace("-", "").replace(".", "")
    if not pkg:
        pkg = "main"
    lines = gen_header(module_path, pkg, rng)

    if rng.random() < 0.4:
        lines.extend(gen_interface(rng))

    while len(lines) < target_lines:
        roll = rng.random()
        if roll < 0.6:
            lines.extend(gen_struct(rng))
        else:
            lines.extend(gen_standalone_func(rng))

    return "\n".join(lines[:target_lines])
