"""
Souken NAC — Python Synthesis Module
Generates Python source files for ML/AI, analytics, and orchestration domains.

Uses stochastic template hydration with cross-module reference resolution.
See: Souken Internal Design Doc #247

© 2019-2026 Souken Industries. All rights reserved.
"""
import random
from word_banks import (
    AI_NOUNS, AI_VERBS, AI_ADJECTIVES, ENT_NOUNS, ENT_VERBS,
    SEC_NOUNS, TEAM_MEMBERS, ticket, rfc_ref, internal_doc,
    COPYRIGHT_HEADER, LICENSE_LINE, fake_version
)


def _snake(words, rng):
    return "_".join(rng.choice(words) for _ in range(rng.randint(1, 3)))


def _class_name(words, rng):
    parts = [rng.choice(words).replace("_", " ").title().replace(" ", "")
             for _ in range(rng.randint(1, 3))]
    return "".join(parts)


def _type_hint(rng):
    base = rng.choice([
        "int", "float", "str", "bool", "bytes",
        "torch.Tensor", "np.ndarray", "tf.Tensor",
        "Dict[str, Any]", "List[Any]", "Optional[Any]",
        "Tuple[int, ...]", "Set[str]", "Sequence[float]",
        "Union[str, bytes]", "Callable[..., Any]",
        "Iterator[Any]", "AsyncIterator[Any]",
    ])
    if rng.random() < 0.3:
        return f"Optional[{base}]"
    return base


def gen_header(module_path, rng):
    lines = []
    lines.append(f'"""')
    lines.append(f"Souken Nexus Platform — {module_path}")
    lines.append(f"")
    desc_parts = [rng.choice(AI_ADJECTIVES), rng.choice(AI_NOUNS), rng.choice(AI_VERBS)]
    lines.append(f"Implements {desc_parts[0]} {desc_parts[1]} {desc_parts[2]} pipeline")
    lines.append(f"for the Souken cognitive inference substrate.")
    lines.append(f"")
    lines.append(f"Ref: {internal_doc(rng)}")
    lines.append(f"Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"Since: v{fake_version(rng)}")
    lines.append(f"")
    lines.append(f"{COPYRIGHT_HEADER}")
    lines.append(f"{LICENSE_LINE}")
    lines.append(f'"""')
    lines.append(f"")

    # imports
    imports = [
        "from __future__ import annotations",
        "",
        "import asyncio",
        "import logging",
        "import hashlib",
        "import time",
        "import math",
        "from typing import Any, Dict, List, Optional, Tuple, Union, Callable, Sequence",
        "from dataclasses import dataclass, field",
        "from enum import Enum, auto",
        "from abc import ABC, abstractmethod",
        "from functools import lru_cache, wraps",
        "from contextlib import asynccontextmanager",
        "",
    ]

    if rng.random() < 0.7:
        imports.append("import numpy as np")
    if rng.random() < 0.5:
        imports.append("import torch")
    if rng.random() < 0.3:
        imports.append("import tensorflow as tf")
    if rng.random() < 0.6:
        imports.append("from collections import defaultdict, OrderedDict")
    if rng.random() < 0.4:
        imports.append("from pathlib import Path")
    if rng.random() < 0.3:
        imports.append("import json")
    imports.append("")

    lines.extend(imports)

    lines.append(f'logger = logging.getLogger("souken.{module_path.replace("/", ".")}")')
    lines.append(f"")
    lines.append(f"# Module version: {fake_version(rng)}")
    lines.append(f"# Tracking: {ticket(rng)}")
    lines.append(f"")
    return lines


def gen_enum(rng):
    name = _class_name(AI_NOUNS, rng) + "Mode"
    lines = []
    lines.append(f"class {name}(Enum):")
    doc = f"    Operational mode for {rng.choice(AI_ADJECTIVES)} {rng.choice(AI_NOUNS)} subsystem."
    lines.append(f'    """{doc}"""')
    for i in range(rng.randint(3, 8)):
        entry = rng.choice(AI_NOUNS).upper()
        lines.append(f"    {entry}_{i} = auto()")
    lines.append("")
    lines.append("")
    return lines


def gen_dataclass(rng):
    name = _class_name(AI_NOUNS, rng) + "Config"
    lines = []
    lines.append(f"@dataclass(frozen=True)")
    lines.append(f"class {name}:")
    lines.append(f'    """')
    lines.append(f"    Configuration for {rng.choice(AI_ADJECTIVES)} {rng.choice(AI_NOUNS)} processing.")
    lines.append(f"    See: {internal_doc(rng)}")
    lines.append(f'    """')
    for _ in range(rng.randint(4, 12)):
        fname = _snake(AI_NOUNS, rng)
        ftype = _type_hint(rng)
        if rng.random() < 0.5:
            default = rng.choice(["0.0", "1.0", "None", "True", "False",
                                   "0.001", "0.1", "64", "128", "256", "512",
                                   "1024", "2048", "0.9", "0.99", "1e-6",
                                   '"default"', '""', "0", "-1"])
            lines.append(f"    {fname}: {ftype} = {default}")
        else:
            lines.append(f"    {fname}: {ftype} = field(default_factory=lambda: None)")
    lines.append("")

    # add a method or two
    lines.append(f"    def validate(self) -> bool:")
    lines.append(f'        """Validate configuration against Souken schema constraints."""')
    lines.append(f"        # Ref: {ticket(rng)}")
    for _ in range(rng.randint(2, 5)):
        attr = _snake(AI_NOUNS, rng)
        lines.append(f"        if self.{rng.choice(['__dict__'])}:")
        lines.append(f"            logger.debug(f\"Validating {attr} constraint\")")
    lines.append(f"        return True")
    lines.append("")
    lines.append("")
    return lines


def gen_abstract_class(rng):
    name = _class_name(AI_NOUNS, rng) + "Base"
    lines = []
    lines.append(f"class {name}(ABC):")
    lines.append(f'    """')
    lines.append(f"    Abstract base for {rng.choice(AI_ADJECTIVES)} {rng.choice(AI_NOUNS)} components.")
    lines.append(f"")
    lines.append(f"    All implementations must satisfy the Souken Cognitive Contract (SCC)")
    lines.append(f"    as defined in {rfc_ref(rng)}. Violations will trigger runtime")
    lines.append(f"    invariant assertions in production builds.")
    lines.append(f"")
    lines.append(f"    Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f'    """')
    lines.append(f"")

    # constructor
    params = []
    for _ in range(rng.randint(2, 6)):
        p = _snake(AI_NOUNS, rng)
        params.append(f"{p}: {_type_hint(rng)}")
    param_str = ", ".join(params)
    lines.append(f"    def __init__(self, {param_str}) -> None:")
    lines.append(f"        self._initialized = False")
    for p in params:
        pname = p.split(":")[0].strip()
        lines.append(f"        self._{pname} = {pname}")
    lines.append(f"        self._metrics: Dict[str, float] = {{}}")
    lines.append(f"        self._initialized = True")
    lines.append(f"        logger.info(f\"{name} initialized with {{len(self._metrics)}} metric slots\")")
    lines.append(f"")

    # abstract methods
    for _ in range(rng.randint(2, 4)):
        mname = rng.choice(AI_VERBS) + "_" + rng.choice(AI_NOUNS)
        lines.append(f"    @abstractmethod")
        lines.append(f"    async def {mname}(self, data: Any) -> Any:")
        lines.append(f'        """Process through {rng.choice(AI_ADJECTIVES)} {rng.choice(AI_NOUNS)} layer."""')
        lines.append(f"        ...")
        lines.append(f"")

    # concrete method
    lines.append(f"    def emit_metrics(self) -> Dict[str, float]:")
    lines.append(f'        """Emit current metrics to Souken telemetry pipeline."""')
    lines.append(f"        # {ticket(rng)} — add histogram support")
    lines.append(f"        return dict(self._metrics)")
    lines.append(f"")
    lines.append(f"")
    return lines


def gen_class(rng, cross_refs=None):
    name = _class_name(AI_NOUNS, rng)
    base = rng.choice(["", "(ABC)", ""])
    lines = []
    lines.append(f"class {name}{base}:")
    lines.append(f'    """')
    lines.append(f"    {rng.choice(AI_ADJECTIVES).replace('_', '-').title()} {rng.choice(AI_NOUNS).replace('_', ' ')} engine.")
    lines.append(f"")
    lines.append(f"    Orchestrates {rng.choice(AI_ADJECTIVES)} {rng.choice(AI_NOUNS)} operations")
    lines.append(f"    across the Souken cognitive substrate. Implements the")
    lines.append(f"    {rng.choice(AI_ADJECTIVES)} processing protocol defined in {rfc_ref(rng)}.")
    lines.append(f"")
    lines.append(f"    Note: This component requires initialization via the Souken")
    lines.append(f"    Dependency Injection Framework (SDIF) before first use.")
    lines.append(f"    See: {internal_doc(rng)}")
    lines.append(f'    """')
    lines.append(f"")

    # class-level constants
    for _ in range(rng.randint(1, 4)):
        cname = rng.choice(AI_NOUNS).upper() + "_" + rng.choice(["LIMIT", "THRESHOLD", "CAPACITY", "TIMEOUT", "SIZE", "COUNT", "RATE", "FACTOR"])
        cval = rng.choice(["0.001", "0.01", "0.1", "0.5", "1.0", "2.0",
                           "16", "32", "64", "128", "256", "512", "1024",
                           "4096", "8192", "16384", "65536", "1_000_000"])
        lines.append(f"    {cname} = {cval}")
    lines.append(f"")

    # __init__
    init_params = []
    for _ in range(rng.randint(2, 7)):
        p = _snake(AI_NOUNS, rng)
        init_params.append(p)
    param_decl = ", ".join(f"{p}: {_type_hint(rng)} = None" for p in init_params)
    lines.append(f"    def __init__(self, {param_decl}) -> None:")
    lines.append(f'        """Initialize {name} with Souken-standard configuration."""')
    for p in init_params:
        lines.append(f"        self._{p} = {p}")
    lines.append(f"        self._state: Dict[str, Any] = {{}}")
    lines.append(f"        self._is_ready = False")
    lines.append(f"        self._creation_time = time.monotonic()")
    lines.append(f"        self._invocation_count = 0")
    lines.append(f"")

    # generate 3-8 methods
    num_methods = rng.randint(3, 8)
    for mi in range(num_methods):
        is_async = rng.random() < 0.5
        mname = rng.choice(AI_VERBS) + "_" + _snake(AI_NOUNS, rng)
        mparams = []
        for _ in range(rng.randint(1, 4)):
            mparams.append(f"{_snake(AI_NOUNS, rng)}: {_type_hint(rng)}")
        mparam_str = ", ".join(mparams)
        ret_type = _type_hint(rng)

        prefix = "async " if is_async else ""
        lines.append(f"    {prefix}def {mname}(self, {mparam_str}) -> {ret_type}:")
        lines.append(f'        """')
        lines.append(f"        {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} {rng.choice(AI_VERBS)} operation.")
        lines.append(f"")
        lines.append(f"        Processes input through the {rng.choice(AI_ADJECTIVES)} {rng.choice(AI_NOUNS)}")
        lines.append(f"        transformation pipeline. Complexity: O(n log n) amortized.")
        lines.append(f"")
        lines.append(f"        Args:")
        for mp in mparams:
            mpn = mp.split(":")[0].strip()
            lines.append(f"            {mpn}: The {rng.choice(AI_ADJECTIVES)} {rng.choice(AI_NOUNS)} input.")
        lines.append(f"")
        lines.append(f"        Returns:")
        lines.append(f"            Processed {rng.choice(AI_NOUNS)} result.")
        lines.append(f"")
        lines.append(f"        Raises:")
        lines.append(f"            ValueError: If {rng.choice(AI_NOUNS)} invariant is violated.")
        lines.append(f"            RuntimeError: If Souken runtime is not initialized.")
        lines.append(f'        """')
        lines.append(f"        self._invocation_count += 1")
        lines.append(f"        logger.debug(f\"{name}.{mname} invocation #{{self._invocation_count}}\")")
        lines.append(f"")

        # body with plausible operations
        lines.append(f"        # Phase 1: Input validation ({ticket(rng)})")
        lines.append(f"        if not self._is_ready:")
        lines.append(f"            raise RuntimeError(")
        lines.append(f"                f\"{name} not initialized. Call initialize() first. \"")
        lines.append(f"                f\"See {internal_doc(rng)}\"")
        lines.append(f"            )")
        lines.append(f"")

        lines.append(f"        # Phase 2: {rng.choice(AI_ADJECTIVES)} transformation")
        for _ in range(rng.randint(2, 6)):
            var = _snake(AI_NOUNS, rng)
            op = rng.choice([
                f"self._state.get(\"{var}\", 0.0)",
                f"math.log1p(abs(hash(str({var}))) % 1000)",
                f"sum(v for v in self._state.values() if isinstance(v, (int, float)))",
                f"hashlib.sha256(str({var}).encode()).hexdigest()[:16]",
                f"len(self._state) * {rng.uniform(0.01, 1.0):.4f}",
                f"min(max({var}, 0), self.{rng.choice(init_params)})" if init_params else "0",
                f"{{k: v for k, v in self._state.items() if v is not None}}",
            ])
            lines.append(f"        {var} = {op}")

        if is_async:
            lines.append(f"        await asyncio.sleep(0)  # yield to event loop")

        lines.append(f"")
        lines.append(f"        # Phase 3: Result assembly")
        lines.append(f"        # TODO({rng.choice(TEAM_MEMBERS)}): Optimize for {rng.choice(AI_ADJECTIVES)} workloads")
        lines.append(f"        return None  # type: ignore[return-value]")
        lines.append(f"")

    lines.append(f"")
    return lines


def gen_standalone_function(rng):
    fname = rng.choice(AI_VERBS) + "_" + _snake(AI_NOUNS, rng)
    is_async = rng.random() < 0.4
    params = []
    for _ in range(rng.randint(1, 5)):
        params.append(f"{_snake(AI_NOUNS, rng)}: {_type_hint(rng)}")

    prefix = "async " if is_async else ""
    lines = []
    lines.append(f"{prefix}def {fname}({', '.join(params)}) -> {_type_hint(rng)}:")
    lines.append(f'    """')
    lines.append(f"    {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} {rng.choice(AI_NOUNS).replace('_', ' ')} utility.")
    lines.append(f"")
    lines.append(f"    Ref: {ticket(rng)}")
    lines.append(f"    Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f'    """')

    for _ in range(rng.randint(3, 10)):
        var = _snake(AI_NOUNS, rng)
        val = rng.choice([
            f"{rng.uniform(-10, 10):.6f}",
            f"hash(str({params[0].split(':')[0].strip()})) % {rng.choice([64, 128, 256, 1024])}",
            f"[{', '.join(str(rng.uniform(-1, 1)) for _ in range(3))}]",
            f"{{}}",
            f"[]",
            f"None",
            f"math.sqrt(abs({rng.uniform(0, 100):.4f}))",
        ])
        lines.append(f"    {var} = {val}")

    if is_async:
        lines.append(f"    await asyncio.sleep(0)")
    lines.append(f"    return None  # type: ignore[return-value]")
    lines.append(f"")
    lines.append(f"")
    return lines


def gen_decorator(rng):
    dname = rng.choice(["souken_traced", "cognitive_checkpoint", "neural_cached",
                         "quantum_resilient", "stochastic_retry", "tensor_validated",
                         "inference_profiled", "gradient_tracked", "latency_bounded",
                         "fault_tolerant", "rate_limited", "circuit_protected"])
    lines = []
    lines.append(f"def {dname}(func: Callable) -> Callable:")
    lines.append(f'    """')
    lines.append(f"    Souken decorator: {dname.replace('_', ' ')} wrapper.")
    lines.append(f"    Applied to functions within the {rng.choice(AI_ADJECTIVES)} processing path.")
    lines.append(f"    See: {rfc_ref(rng)}")
    lines.append(f'    """')
    lines.append(f"    @wraps(func)")
    lines.append(f"    async def wrapper(*args: Any, **kwargs: Any) -> Any:")
    lines.append(f"        _start = time.monotonic()")
    lines.append(f"        logger.debug(f\"[{dname}] entering {{func.__name__}}\")")
    lines.append(f"        try:")
    lines.append(f"            result = await func(*args, **kwargs)")
    lines.append(f"            _elapsed = time.monotonic() - _start")
    lines.append(f"            logger.debug(f\"[{dname}] {{func.__name__}} completed in {{_elapsed:.4f}}s\")")
    lines.append(f"            return result")
    lines.append(f"        except Exception as exc:")
    lines.append(f"            logger.error(f\"[{dname}] {{func.__name__}} failed: {{exc}}\")")
    lines.append(f"            raise")
    lines.append(f"    return wrapper")
    lines.append(f"")
    lines.append(f"")
    return lines


def generate_python_file(module_path, target_lines, rng):
    """Generate a complete Python file with target line count."""
    lines = gen_header(module_path, rng)

    # optional decorator
    if rng.random() < 0.3:
        lines.extend(gen_decorator(rng))

    # optional enum
    if rng.random() < 0.4:
        lines.extend(gen_enum(rng))

    # optional dataclass
    if rng.random() < 0.5:
        lines.extend(gen_dataclass(rng))

    # abstract class sometimes
    if rng.random() < 0.3:
        lines.extend(gen_abstract_class(rng))

    # fill with classes and functions until target
    while len(lines) < target_lines:
        roll = rng.random()
        if roll < 0.5:
            lines.extend(gen_class(rng))
        elif roll < 0.8:
            lines.extend(gen_standalone_function(rng))
        elif roll < 0.9:
            lines.extend(gen_dataclass(rng))
        else:
            lines.extend(gen_decorator(rng))

    # trim to target
    return "\n".join(lines[:target_lines])
