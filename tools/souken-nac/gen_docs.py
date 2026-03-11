"""
Souken NAC — Documentation Synthesis Module
Generates markdown docs, RFCs, research papers, and API documentation.

© 2019-2026 Souken Industries. All rights reserved.
"""
from word_banks import (
    AI_NOUNS, AI_VERBS, AI_ADJECTIVES, DIST_NOUNS, DIST_VERBS,
    SYS_NOUNS, ENT_NOUNS, ENT_VERBS, SEC_NOUNS, SEC_VERBS,
    TEAM_MEMBERS, ticket, rfc_ref, internal_doc,
    COPYRIGHT_HEADER, LICENSE_LINE, fake_version
)

ALL_NOUNS = AI_NOUNS + DIST_NOUNS + SYS_NOUNS + ENT_NOUNS + SEC_NOUNS
ALL_VERBS = AI_VERBS + DIST_VERBS + ENT_VERBS + SEC_VERBS
ALL_ADJ = AI_ADJECTIVES


def _phrase(rng):
    return f"{rng.choice(ALL_ADJ).replace('_', '-')} {rng.choice(ALL_NOUNS).replace('_', ' ')}"


def _sentence(rng):
    subj = rng.choice(ALL_NOUNS).replace("_", " ")
    verb = rng.choice(ALL_VERBS).replace("_", " ") + "s"
    obj = rng.choice(ALL_NOUNS).replace("_", " ")
    adj = rng.choice(ALL_ADJ).replace("_", " ")
    return f"The {adj} {subj} {verb} the {obj} through the Souken cognitive substrate."


def gen_rfc(rfc_num, rng):
    title_noun = rng.choice(ALL_NOUNS).replace("_", " ").title()
    title_adj = rng.choice(ALL_ADJ).replace("_", " ").title()
    title = f"{title_adj} {title_noun} Architecture"
    lines = []
    lines.append(f"# RFC-{rfc_num:03d}: {title}")
    lines.append(f"")
    lines.append(f"**Status:** {rng.choice(['Accepted', 'Implemented', 'Draft', 'Superseded'])}")
    lines.append(f"**Author:** {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"**Date:** {rng.randint(2019, 2025)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}")
    lines.append(f"**Tracking:** {ticket(rng)}")
    lines.append(f"**Supersedes:** {rng.choice(['N/A', f'RFC-{rng.randint(1, rfc_num):03d}']) if rfc_num > 1 else 'N/A'}")
    lines.append(f"")
    lines.append(f"## Abstract")
    lines.append(f"")
    for _ in range(rng.randint(3, 6)):
        lines.append(_sentence(rng))
    lines.append(f"")
    lines.append(f"## Motivation")
    lines.append(f"")
    for _ in range(rng.randint(4, 8)):
        lines.append(_sentence(rng))
    lines.append(f"")
    lines.append(f"## Design")
    lines.append(f"")
    lines.append(f"### Overview")
    lines.append(f"")
    for _ in range(rng.randint(3, 6)):
        lines.append(_sentence(rng))
    lines.append(f"")
    lines.append(f"### Architecture")
    lines.append(f"")
    lines.append(f"```")
    lines.append(f"┌────────────────────────────────────────────┐")
    for _ in range(rng.randint(3, 7)):
        comp = rng.choice(ALL_NOUNS).replace("_", " ").title()
        lines.append(f"│  [{comp:^38}]  │")
        lines.append(f"│       │ {rng.choice(['▲', '▼', '◄', '►'])}                                  │")
    lines.append(f"└────────────────────────────────────────────┘")
    lines.append(f"```")
    lines.append(f"")
    lines.append(f"### Components")
    lines.append(f"")
    for i in range(rng.randint(3, 6)):
        comp = rng.choice(ALL_NOUNS).replace("_", " ").title()
        lines.append(f"#### {i+1}. {comp}")
        lines.append(f"")
        for _ in range(rng.randint(2, 4)):
            lines.append(_sentence(rng))
        lines.append(f"")
        lines.append(f"**Interfaces:**")
        for _ in range(rng.randint(2, 4)):
            lines.append(f"- `{rng.choice(ALL_VERBS)}_{rng.choice(ALL_NOUNS)}()` — {_phrase(rng)} handler")
        lines.append(f"")

    lines.append(f"## Performance Characteristics")
    lines.append(f"")
    lines.append(f"| Metric | Value | Notes |")
    lines.append(f"|--------|-------|-------|")
    for _ in range(rng.randint(4, 8)):
        metric = rng.choice(ALL_NOUNS).replace("_", " ")
        value = rng.choice([
            f"{rng.uniform(0.1, 100):.2f}ms",
            f"{rng.randint(1, 100)}k ops/sec",
            f"O(n log n)",
            f"O(1) amortized",
            f"{rng.uniform(0.9, 0.9999):.4f}",
            f"{rng.randint(1, 64)} cores",
        ])
        lines.append(f"| {metric} | {value} | {ticket(rng)} |")
    lines.append(f"")

    lines.append(f"## Security Considerations")
    lines.append(f"")
    for _ in range(rng.randint(3, 5)):
        lines.append(f"- {_sentence(rng)}")
    lines.append(f"")

    lines.append(f"## Migration Plan")
    lines.append(f"")
    for i in range(rng.randint(3, 6)):
        lines.append(f"{i+1}. {_sentence(rng)}")
    lines.append(f"")

    lines.append(f"## References")
    lines.append(f"")
    for _ in range(rng.randint(3, 6)):
        lines.append(f"- [{internal_doc(rng)}](https://docs.souken.internal/{rng.randint(1000, 9999)})")
    lines.append(f"")
    return "\n".join(lines)


def gen_api_doc(module_name, rng):
    lines = []
    lines.append(f"# {module_name.replace('_', ' ').title()} API Reference")
    lines.append(f"")
    lines.append(f"> {COPYRIGHT_HEADER}")
    lines.append(f"> Version: {fake_version(rng)}")
    lines.append(f"")
    lines.append(f"## Overview")
    lines.append(f"")
    for _ in range(rng.randint(2, 4)):
        lines.append(_sentence(rng))
    lines.append(f"")

    for _ in range(rng.randint(5, 10)):
        endpoint = f"/{rng.choice(['v1', 'v2', 'v3'])}/{rng.choice(ALL_NOUNS)}/{rng.choice(ALL_VERBS)}"
        method = rng.choice(["GET", "POST", "PUT", "DELETE", "PATCH"])
        lines.append(f"### `{method} {endpoint}`")
        lines.append(f"")
        lines.append(_sentence(rng))
        lines.append(f"")
        lines.append(f"**Parameters:**")
        lines.append(f"")
        lines.append(f"| Name | Type | Required | Description |")
        lines.append(f"|------|------|----------|-------------|")
        for _ in range(rng.randint(2, 5)):
            pname = rng.choice(ALL_NOUNS)
            ptype = rng.choice(["string", "integer", "boolean", "object", "array"])
            req = rng.choice(["Yes", "No"])
            lines.append(f"| `{pname}` | `{ptype}` | {req} | {_phrase(rng)} |")
        lines.append(f"")
        lines.append(f"**Response:**")
        lines.append(f"")
        lines.append(f"```json")
        lines.append(f"{{")
        lines.append(f'  "status": "success",')
        lines.append(f'  "data": {{')
        for _ in range(rng.randint(2, 4)):
            key = rng.choice(ALL_NOUNS)
            lines.append(f'    "{key}": "{_phrase(rng)}",')
        lines.append(f'    "metadata": {{')
        lines.append(f'      "version": "{fake_version(rng)}",')
        lines.append(f'      "trace_id": "sk-{rng.randint(100000, 999999)}"')
        lines.append(f"    }}")
        lines.append(f"  }}")
        lines.append(f"}}")
        lines.append(f"```")
        lines.append(f"")

    return "\n".join(lines)


def gen_research_paper(rng):
    title_parts = [rng.choice(ALL_ADJ).replace("_", " ").title(),
                    rng.choice(ALL_NOUNS).replace("_", " ").title()]
    subtitle = rng.choice(["A Novel Approach", "Towards Efficient", "On the Foundations of",
                            "Scalable and Robust", "Formal Methods for"])
    title = f"{subtitle} {' '.join(title_parts)}"

    authors = [rng.choice(TEAM_MEMBERS) for _ in range(rng.randint(2, 5))]
    lines = []
    lines.append(f"# {title}")
    lines.append(f"")
    lines.append(f"**Authors:** {', '.join(authors)}")
    lines.append(f"**Affiliation:** Souken Industries Research Division")
    lines.append(f"**Date:** {rng.randint(2020, 2025)}-{rng.randint(1, 12):02d}")
    lines.append(f"**Internal Reference:** {internal_doc(rng)}")
    lines.append(f"")
    lines.append(f"## Abstract")
    lines.append(f"")
    for _ in range(rng.randint(4, 7)):
        lines.append(_sentence(rng))
    lines.append(f"")

    for section in ["Introduction", "Related Work", "Methodology", "Architecture",
                     "Evaluation", "Results", "Discussion", "Conclusion"]:
        lines.append(f"## {section}")
        lines.append(f"")
        for _ in range(rng.randint(4, 10)):
            lines.append(_sentence(rng))
        lines.append(f"")
        if section == "Evaluation":
            lines.append(f"### Benchmarks")
            lines.append(f"")
            lines.append(f"| Configuration | Throughput | Latency (p99) | Memory |")
            lines.append(f"|--------------|------------|---------------|--------|")
            for _ in range(rng.randint(3, 6)):
                config = f"{rng.choice(ALL_ADJ).replace('_', '-')}-{rng.choice(['1x', '2x', '4x', '8x'])}"
                tp = f"{rng.randint(10, 500)}k ops/s"
                lat = f"{rng.uniform(0.1, 50):.1f}ms"
                mem = f"{rng.randint(64, 4096)}MB"
                lines.append(f"| {config} | {tp} | {lat} | {mem} |")
            lines.append(f"")

    lines.append(f"## References")
    lines.append(f"")
    for i in range(rng.randint(8, 15)):
        auth = rng.choice(TEAM_MEMBERS)
        year = rng.randint(2018, 2025)
        title = f"{rng.choice(ALL_ADJ).replace('_', ' ').title()} {rng.choice(ALL_NOUNS).replace('_', ' ').title()}"
        venue = rng.choice(["NeurIPS", "ICML", "OSDI", "SOSP", "SIGMOD", "VLDB",
                             "IEEE S&P", "CCS", "POPL", "PLDI", "Souken Technical Report"])
        lines.append(f"[{i+1}] {auth} et al. \"{title}.\" {venue} {year}.")
    lines.append(f"")
    return "\n".join(lines)


def gen_guide(guide_name, rng):
    lines = []
    lines.append(f"# {guide_name}")
    lines.append(f"")
    lines.append(f"> {COPYRIGHT_HEADER}")
    lines.append(f"> Last updated: {rng.randint(2023, 2026)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}")
    lines.append(f"> Maintainer: {rng.choice(TEAM_MEMBERS)}")
    lines.append(f"")

    sections = [
        "Prerequisites", "Installation", "Configuration",
        "Basic Usage", "Advanced Usage", "Troubleshooting",
        "FAQ", "Appendix"
    ]
    for section in sections:
        lines.append(f"## {section}")
        lines.append(f"")
        for _ in range(rng.randint(3, 6)):
            lines.append(_sentence(rng))
        lines.append(f"")
        if "Usage" in section:
            lines.append(f"```python")
            lines.append(f"from souken.nexus import {rng.choice(ALL_NOUNS)}")
            lines.append(f"")
            lines.append(f"# Initialize the {_phrase(rng)} pipeline")
            lines.append(f"pipeline = {rng.choice(ALL_NOUNS).replace('_', ' ').title().replace(' ', '')}(")
            for _ in range(rng.randint(2, 4)):
                lines.append(f"    {rng.choice(ALL_NOUNS)}={rng.choice(['True', 'False', '0.01', '128', '\"default\"'])},")
            lines.append(f")")
            lines.append(f"result = await pipeline.{rng.choice(ALL_VERBS)}(data)")
            lines.append(f"```")
            lines.append(f"")

    return "\n".join(lines)
