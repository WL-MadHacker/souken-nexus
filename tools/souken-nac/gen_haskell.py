"""
Souken NAC — Haskell Synthesis Module
Generates Haskell source files for formal verification and cognitive bridge domains.

© 2019-2026 Souken Industries. All rights reserved.
"""
from word_banks import (
    AI_NOUNS, AI_VERBS, AI_ADJECTIVES, SEC_NOUNS, SEC_VERBS,
    TEAM_MEMBERS, ticket, rfc_ref, internal_doc,
    COPYRIGHT_HEADER, LICENSE_LINE, fake_version
)

ALL_NOUNS = AI_NOUNS + SEC_NOUNS


def _pascal(words, rng):
    return "".join(rng.choice(words).replace("_", " ").title().replace(" ", "")
                   for _ in range(rng.randint(1, 2)))


def _lower(words, rng):
    w = rng.choice(words)
    parts = w.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


def _hs_type(rng):
    base = rng.choice([
        "Int", "Integer", "Double", "Float", "Bool", "Text",
        "ByteString", "Natural", "Word64",
    ])
    wrapper = rng.choice([
        "{}", "Maybe {}", "Either Text {}", "IO {}", "STM {}",
        "[{}]", "Map Text {}", "Set {}", "Vector {}",
        "ReaderT Config IO {}", "StateT {} IO ()",
    ])
    return wrapper.format(base)


def gen_header(module_path, rng):
    mod_name = "Souken." + ".".join(
        p.replace("_", " ").title().replace(" ", "")
        for p in module_path.split("/") if p
    )
    lines = []
    lines.append(f"-- |")
    lines.append(f"-- Module      : {mod_name}")
    lines.append(f"-- {COPYRIGHT_HEADER}")
    lines.append(f"-- {LICENSE_LINE}")
    lines.append(f"--")
    lines.append(f"-- {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} {rng.choice(AI_NOUNS).replace('_', ' ')} module")
    lines.append(f"-- for the Souken Cognitive Bridge formal verification subsystem.")
    lines.append(f"--")
    lines.append(f"-- Implements {rng.choice(AI_ADJECTIVES).replace('_', ' ')} type-level guarantees")
    lines.append(f"-- for {rng.choice(SEC_NOUNS).replace('_', ' ')} integrity.")
    lines.append(f"--")
    lines.append(f"-- Ref: {internal_doc(rng)}")
    lines.append(f"-- Author: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"-- Tracking: {ticket(rng)}")
    lines.append(f"")
    lines.append(f"{{-# LANGUAGE GADTs #-}}")
    lines.append(f"{{-# LANGUAGE DataKinds #-}}")
    lines.append(f"{{-# LANGUAGE TypeFamilies #-}}")
    lines.append(f"{{-# LANGUAGE RankNTypes #-}}")
    lines.append(f"{{-# LANGUAGE ScopedTypeVariables #-}}")
    lines.append(f"{{-# LANGUAGE OverloadedStrings #-}}")
    lines.append(f"{{-# LANGUAGE DeriveGeneric #-}}")
    lines.append(f"{{-# LANGUAGE DerivingStrategies #-}}")
    lines.append(f"{{-# LANGUAGE GeneralizedNewtypeDeriving #-}}")
    if rng.random() < 0.5:
        lines.append(f"{{-# LANGUAGE MultiParamTypeClasses #-}}")
        lines.append(f"{{-# LANGUAGE FunctionalDependencies #-}}")
    if rng.random() < 0.3:
        lines.append(f"{{-# LANGUAGE TypeOperators #-}}")
        lines.append(f"{{-# LANGUAGE ConstraintKinds #-}}")
    lines.append(f"")
    lines.append(f"module {mod_name}")
    # exports
    exports = []
    for _ in range(rng.randint(3, 8)):
        exports.append(_pascal(ALL_NOUNS, rng))
    lines.append(f"  ( {', '.join(exports)}")
    lines.append(f"  ) where")
    lines.append(f"")

    imports = [
        "import Data.Text (Text)",
        "import qualified Data.Text as T",
        "import Data.Map.Strict (Map)",
        "import qualified Data.Map.Strict as Map",
        "import Data.Set (Set)",
        "import qualified Data.Set as Set",
        "import Data.Maybe (fromMaybe, isJust)",
        "import Control.Monad (when, unless, void, forM_)",
        "import Control.Monad.IO.Class (MonadIO, liftIO)",
        "import GHC.Generics (Generic)",
        "import Data.Hashable (Hashable)",
    ]
    if rng.random() < 0.5:
        imports.append("import Control.Concurrent.STM")
        imports.append("import Control.Concurrent.STM.TVar")
    if rng.random() < 0.4:
        imports.append("import Data.IORef")
    if rng.random() < 0.3:
        imports.append("import qualified Data.ByteString as BS")
        imports.append("import qualified Data.ByteString.Lazy as BL")
    imports.append(f"import qualified Souken.Core.{_pascal(ALL_NOUNS, rng)} as SC")
    imports.append(f"import Souken.Types ({', '.join(_pascal(ALL_NOUNS, rng) for _ in range(2))})")

    for imp in imports:
        lines.append(imp)
    lines.append(f"")
    return lines


def gen_newtype(rng):
    name = _pascal(ALL_NOUNS, rng)
    inner = rng.choice(["Int", "Integer", "Double", "Text", "ByteString", "Word64", "Natural"])
    lines = []
    lines.append(f"-- | {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} wrapper for {rng.choice(AI_NOUNS).replace('_', ' ')}.")
    lines.append(f"-- Enforces Souken type-level invariants. See: {rfc_ref(rng)}")
    lines.append(f"newtype {name} = {name}")
    lines.append(f"  {{ un{name} :: {inner}")
    lines.append(f"  }} deriving stock (Show, Eq, Ord, Generic)")
    lines.append(f"     deriving newtype (Hashable)")
    lines.append(f"")
    return lines


def gen_data_type(rng):
    name = _pascal(ALL_NOUNS, rng)
    lines = []
    lines.append(f"-- | Algebraic data type for {rng.choice(AI_NOUNS).replace('_', ' ')} states.")
    lines.append(f"-- Part of the Souken Cognitive Bridge type system.")
    lines.append(f"-- Ref: {ticket(rng)}")
    lines.append(f"data {name}")
    variants = []
    for i in range(rng.randint(3, 7)):
        vname = _pascal(ALL_NOUNS, rng) + rng.choice(["State", "Phase", "Mode", "Signal"])
        fields = []
        for _ in range(rng.randint(0, 3)):
            fields.append(rng.choice(["Int", "Double", "Text", "Bool", "[Text]", "Map Text Double"]))
        if fields:
            variants.append(f"  {'= ' if i == 0 else '| '}{vname} {' '.join(fields)}")
        else:
            variants.append(f"  {'= ' if i == 0 else '| '}{vname}")
    lines.extend(variants)
    lines.append(f"  deriving (Show, Eq, Generic)")
    lines.append(f"")
    return lines


def gen_typeclass(rng):
    name = _pascal(ALL_NOUNS, rng) + "able"
    lines = []
    lines.append(f"-- | Type class for {rng.choice(AI_ADJECTIVES).replace('_', ' ')} {rng.choice(AI_NOUNS).replace('_', ' ')} operations.")
    lines.append(f"-- All Souken cognitive components must implement this contract.")
    lines.append(f"-- See: {rfc_ref(rng)}")
    lines.append(f"class {name} a where")
    for _ in range(rng.randint(2, 5)):
        mname = _lower(AI_VERBS, rng)
        lines.append(f"  -- | {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} {mname} operation.")
        lines.append(f"  {mname} :: a -> {_hs_type(rng)}")
    lines.append(f"")
    return lines


def gen_function(rng):
    fname = _lower(AI_VERBS, rng) + _pascal(ALL_NOUNS, rng)
    lines = []
    lines.append(f"-- | {rng.choice(AI_ADJECTIVES).replace('_', ' ').title()} {rng.choice(AI_NOUNS).replace('_', ' ')} transformation.")
    lines.append(f"-- Complexity: O(n log n) amortized.")
    lines.append(f"-- Author: {rng.choice(TEAM_MEMBERS)} | {ticket(rng)}")
    param_types = [rng.choice(["Int", "Double", "Text", "Bool", "[Int]", "Map Text Double"]) for _ in range(rng.randint(1, 3))]
    ret = rng.choice(["Int", "Double", "Text", "Bool", "Maybe Int", "Either Text Double", "[Text]"])
    sig = " -> ".join(param_types + [ret])
    lines.append(f"{fname} :: {sig}")

    params = [f"x{i}" for i in range(len(param_types))]
    lines.append(f"{fname} {' '.join(params)} =")

    # body
    body_style = rng.choice(["let", "where", "case", "guards"])
    if body_style == "let":
        lines.append(f"  let")
        for _ in range(rng.randint(2, 5)):
            var = _lower(AI_NOUNS, rng)
            val = rng.choice([
                f"fromMaybe 0 (Just ({params[0]} + 1))" if "Int" in param_types[0] else f'T.pack "{rng.choice(AI_NOUNS)}"',
                f"Map.empty",
                f"Set.empty",
                f"{rng.randint(0, 1000)}",
                f"{rng.uniform(-1, 1):.6f}",
            ])
            lines.append(f"    {var} = {val}")
        lines.append(f"  in {rng.choice(['0', '0.0', 'T.empty', 'True', 'Nothing', 'Right 0.0', '[]'])}")
    elif body_style == "where":
        lines.append(f"  result")
        lines.append(f"  where")
        for _ in range(rng.randint(2, 4)):
            var = _lower(AI_NOUNS, rng)
            lines.append(f"    {var} = {rng.randint(0, 1000)}")
        lines.append(f"    result = {rng.choice(['0', '0.0', 'T.empty', 'True', 'Nothing', 'Right 0.0', '[]'])}")
    elif body_style == "case":
        lines.append(f"  case {params[0]} of")
        for _ in range(rng.randint(2, 4)):
            pat = rng.choice(["_", "0", "1", "True", "False", '""'])
            lines.append(f"    {pat} -> {rng.choice(['0', '0.0', 'T.empty', 'True', 'Nothing', 'Right 0.0', '[]'])}")
        lines.append(f"    _ -> {rng.choice(['0', '0.0', 'T.empty', 'True', 'Nothing', 'Right 0.0', '[]'])}")
    else:
        lines.append(f"  | {params[0]} == {params[0]} = {rng.choice(['0', '0.0', 'T.empty', 'True', 'Nothing', 'Right 0.0', '[]'])}")
        lines.append(f"  | otherwise = {rng.choice(['0', '0.0', 'T.empty', 'True', 'Nothing', 'Right 0.0', '[]'])}")

    lines.append(f"")
    return lines


def generate_haskell_file(module_path, target_lines, rng):
    lines = gen_header(module_path, rng)

    for _ in range(rng.randint(1, 3)):
        lines.extend(gen_newtype(rng))

    if rng.random() < 0.5:
        lines.extend(gen_data_type(rng))

    if rng.random() < 0.4:
        lines.extend(gen_typeclass(rng))

    while len(lines) < target_lines:
        roll = rng.random()
        if roll < 0.5:
            lines.extend(gen_function(rng))
        elif roll < 0.7:
            lines.extend(gen_data_type(rng))
        elif roll < 0.85:
            lines.extend(gen_newtype(rng))
        else:
            lines.extend(gen_typeclass(rng))

    return "\n".join(lines[:target_lines])
