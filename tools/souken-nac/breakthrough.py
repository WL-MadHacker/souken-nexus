"""
Souken NAC — Breakthrough Publication Engine v1.0
Generates research artifacts (papers, RFCs, code) and ships them
as branches → PRs → auto-merged into master.

Part of the Souken Neural Architecture Compiler toolchain.
© 2019-2026 Souken Industries. All rights reserved.
"""

import json
import os
import random
import re
import shutil
import subprocess
import sys
import time

# Ensure we can import sibling modules
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from word_banks import (
    AI_NOUNS, AI_VERBS, AI_ADJECTIVES, DIST_NOUNS, ENT_NOUNS,
    SYS_NOUNS, SEC_NOUNS, TEAM_MEMBERS, ticket, internal_doc,
    COPYRIGHT_HEADER, fake_version
)
from gen_docs import gen_research_paper, gen_rfc
from gen_python import generate_python_file
from gen_rust import generate_rust_file
from gen_typescript import generate_typescript_file
from gen_go import generate_go_file

ALL_NOUNS = AI_NOUNS + DIST_NOUNS + SYS_NOUNS + ENT_NOUNS + SEC_NOUNS
ALL_ADJ = AI_ADJECTIVES

# Repo root (two levels up from tools/souken-nac/)
REPO_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
STATE_FILE = os.path.join(_THIS_DIR, ".breakthrough_state.json")
UPLOADS_DIR = os.path.join(_THIS_DIR, "uploads")

# Artifact types cycle
ARTIFACT_TYPES = ["paper", "rfc", "code"]

# Module paths where code artifacts can land
CODE_TARGETS = [
    ("nexus/orchestrator/src", "python", "Model orchestration"),
    ("nexus/training/src", "python", "Training pipelines"),
    ("nexus/neural_mesh/src", "python", "Neural mesh networking"),
    ("platform/api_gateway/src", "go", "API gateway"),
    ("platform/auth/src", "typescript", "Auth service"),
    ("platform/analytics/src", "python", "Analytics pipeline"),
    ("distributed/consensus/src", "rust", "Consensus algorithm"),
    ("distributed/sharding/src", "go", "Data sharding"),
    ("distributed/mesh/src", "rust", "Service mesh"),
    ("core/runtime/src", "rust", "Runtime engine"),
    ("sdk/python/souken", "python", "Python SDK"),
    ("sdk/typescript/src", "typescript", "TypeScript SDK"),
]

CODE_GENERATORS = {
    "python": generate_python_file,
    "rust": generate_rust_file,
    "typescript": generate_typescript_file,
    "go": generate_go_file,
}


def load_state():
    """Load breakthrough state, or create defaults."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "last_type_index": -1,
        "next_rfc": 51,
        "next_tr": 17,
        "run_count": 0,
    }


def save_state(state):
    """Persist state to disk."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def _slugify(text, max_len=40):
    """Convert text to a URL/branch-safe slug."""
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return slug[:max_len].rstrip('-')


def generate_breakthrough(state=None, image_path=None, mermaid_code=None, feedback=None):
    """
    Generate a new breakthrough artifact.
    Returns a dict with: type, content, summary, metadata, files_to_commit
    """
    if state is None:
        state = load_state()

    # Advance the cycle
    type_index = (state["last_type_index"] + 1) % len(ARTIFACT_TYPES)
    artifact_type = ARTIFACT_TYPES[type_index]

    # Use time-based seed for variety
    rng = random.Random(int(time.time() * 1000) + state["run_count"])

    result = {
        "type": artifact_type,
        "content": "",
        "summary": {},
        "metadata": {},
        "files_to_commit": [],  # list of (repo_relative_path, content_or_None_for_binary)
    }

    if artifact_type == "paper":
        result = _generate_paper(rng, state, image_path, mermaid_code)
    elif artifact_type == "rfc":
        result = _generate_rfc(rng, state, image_path, mermaid_code)
    elif artifact_type == "code":
        result = _generate_code(rng, state)

    result["state_update"] = {
        "last_type_index": type_index,
        "next_rfc": state["next_rfc"] + (1 if artifact_type == "rfc" else 0),
        "next_tr": state["next_tr"] + (1 if artifact_type == "paper" else 0),
        "run_count": state["run_count"] + 1,
    }

    return result


def _generate_paper(rng, state, image_path=None, mermaid_code=None):
    """Generate a research paper artifact."""
    tr_num = state["next_tr"]
    content = gen_research_paper(rng)

    # Extract title from first line
    title_line = content.split("\n")[0].replace("# ", "")
    slug = _slugify(title_line)

    # Inject image if provided
    if image_path:
        ext = os.path.splitext(image_path)[1]
        fig_filename = f"tr-2026-{tr_num:03d}-fig1{ext}"
        fig_caption = f"{rng.choice(ALL_ADJ).replace('_', ' ').title()} {rng.choice(ALL_NOUNS).replace('_', ' ')} — Experimental Results"
        fig_md = f"\n\n![Figure 1: {fig_caption}](figures/{fig_filename})\n"
        # Insert after ## Results section
        if "## Results" in content:
            content = content.replace("## Results", f"## Results\n{fig_md}", 1)
        else:
            content = content.replace("## Evaluation", f"## Evaluation\n{fig_md}", 1)

    # Inject mermaid diagram if provided
    if mermaid_code:
        mermaid_block = f"\n\n### System Architecture\n\n```mermaid\n{mermaid_code.strip()}\n```\n"
        if "## Architecture" in content:
            content = content.replace("## Architecture", f"## Architecture\n{mermaid_block}", 1)
        elif "## Methodology" in content:
            content = content.replace("## Methodology", f"## Methodology\n{mermaid_block}", 1)

    file_path = f"docs/papers/souken-tr-2026-{tr_num:03d}.md"
    files = [(file_path, content)]

    if image_path:
        fig_dir = "docs/papers/figures"
        files.append((f"{fig_dir}/{fig_filename}", None))  # binary copy

    # Extract summary
    abstract_lines = []
    in_abstract = False
    for line in content.split("\n"):
        if line.strip() == "## Abstract":
            in_abstract = True
            continue
        if in_abstract and line.startswith("## "):
            break
        if in_abstract and line.strip():
            abstract_lines.append(line.strip())

    authors_line = ""
    for line in content.split("\n"):
        if line.startswith("**Authors:**"):
            authors_line = line.replace("**Authors:**", "").strip()
            break

    summary = {
        "title": title_line,
        "authors": authors_line,
        "abstract": " ".join(abstract_lines[:3]),
        "cliff_notes": [
            f"Proposes a novel approach to {rng.choice(ALL_NOUNS).replace('_', ' ')} using {rng.choice(ALL_ADJ).replace('_', ' ')} techniques",
            f"Benchmarks show {rng.uniform(1.5, 12.0):.1f}x improvement over baseline on {rng.choice(ALL_NOUNS).replace('_', ' ')} workloads",
            f"Extends prior work from {rng.choice(TEAM_MEMBERS)} et al. on {rng.choice(ALL_NOUNS).replace('_', ' ')} optimization",
        ],
    }

    metadata = {
        "branch": f"research/tr-2026-{tr_num:03d}-{slug}",
        "commit_msg": f"docs: publish TR-2026-{tr_num:03d} — {title_line}",
        "pr_title": f"[Research] TR-2026-{tr_num:03d}: {title_line}",
        "pr_body": _paper_pr_body(title_line, authors_line, summary, tr_num, rng),
        "file_path": file_path,
    }

    return {
        "type": "paper",
        "content": content,
        "summary": summary,
        "metadata": metadata,
        "files_to_commit": files,
        "image_path": image_path,
    }


def _generate_rfc(rng, state, image_path=None, mermaid_code=None):
    """Generate an RFC artifact."""
    rfc_num = state["next_rfc"]
    content = gen_rfc(rfc_num, rng)

    title_line = content.split("\n")[0].replace(f"# RFC-{rfc_num:03d}: ", "")
    slug = _slugify(title_line)

    # Inject image
    if image_path:
        ext = os.path.splitext(image_path)[1]
        fig_filename = f"rfc-{rfc_num:03d}-fig1{ext}"
        fig_caption = f"{rng.choice(ALL_ADJ).replace('_', ' ').title()} {rng.choice(ALL_NOUNS).replace('_', ' ')} — Architecture Overview"
        fig_md = f"\n\n![Figure 1: {fig_caption}](figures/{fig_filename})\n"
        if "### Architecture" in content:
            content = content.replace("### Architecture", f"### Architecture\n{fig_md}", 1)

    # Inject mermaid
    if mermaid_code:
        mermaid_block = f"\n\n```mermaid\n{mermaid_code.strip()}\n```\n"
        if "### Overview" in content:
            content = content.replace("### Overview", f"### Overview\n{mermaid_block}", 1)

    file_path = f"docs/rfcs/RFC-{rfc_num:03d}-{slug}.md"
    files = [(file_path, content)]

    if image_path:
        fig_dir = "docs/rfcs/figures"
        ext = os.path.splitext(image_path)[1]
        fig_filename = f"rfc-{rfc_num:03d}-fig1{ext}"
        files.append((f"{fig_dir}/{fig_filename}", None))

    # Extract summary
    abstract_lines = []
    in_abstract = False
    for line in content.split("\n"):
        if line.strip() == "## Abstract":
            in_abstract = True
            continue
        if in_abstract and line.startswith("## "):
            break
        if in_abstract and line.strip():
            abstract_lines.append(line.strip())

    status_line = ""
    author_line = ""
    for line in content.split("\n"):
        if line.startswith("**Status:**"):
            status_line = line.replace("**Status:**", "").strip()
        if line.startswith("**Author:**"):
            author_line = line.replace("**Author:**", "").strip()

    summary = {
        "title": f"RFC-{rfc_num:03d}: {title_line}",
        "authors": author_line,
        "status": status_line,
        "abstract": " ".join(abstract_lines[:3]),
        "cliff_notes": [
            f"Proposes new {rng.choice(ALL_NOUNS).replace('_', ' ')} architecture for the Souken platform",
            f"Addresses performance bottleneck in {rng.choice(ALL_NOUNS).replace('_', ' ')} subsystem ({ticket(rng)})",
            f"Migration plan spans {rng.randint(2, 6)} phases with backward compatibility guarantees",
        ],
    }

    metadata = {
        "branch": f"rfc/{rfc_num:03d}-{slug}",
        "commit_msg": f"rfc: propose RFC-{rfc_num:03d} — {title_line}",
        "pr_title": f"[RFC] RFC-{rfc_num:03d}: {title_line}",
        "pr_body": _rfc_pr_body(title_line, rfc_num, summary, rng),
        "file_path": file_path,
    }

    return {
        "type": "rfc",
        "content": content,
        "summary": summary,
        "metadata": metadata,
        "files_to_commit": files,
        "image_path": image_path,
    }


def _generate_code(rng, state):
    """Generate a code artifact (new source file in an existing module)."""
    target = rng.choice(CODE_TARGETS)
    path_prefix, lang, domain = target

    gen_fn = CODE_GENERATORS.get(lang)
    if not gen_fn:
        # Fallback to python
        gen_fn = generate_python_file
        lang = "python"

    # Generate a filename
    noun1 = rng.choice(ALL_NOUNS)
    noun2 = rng.choice(ALL_NOUNS)
    filename_stem = f"{noun1}_{noun2}"

    ext_map = {"python": ".py", "typescript": ".ts", "rust": ".rs", "go": ".go"}
    ext = ext_map.get(lang, ".py")

    module_path = f"{path_prefix}/{filename_stem}"
    target_lines = rng.randint(200, 500)
    content = gen_fn(module_path, target_lines, rng)

    file_path = f"{path_prefix}/{filename_stem}{ext}"
    verb = rng.choice(["implement", "add", "introduce", "create"])
    description = f"{rng.choice(ALL_ADJ).replace('_', ' ')} {noun1.replace('_', ' ')} {rng.choice(AI_VERBS).replace('_', ' ')} pipeline"
    module_name = path_prefix.split("/")[0]

    slug = _slugify(f"{noun1}-{noun2}")

    summary = {
        "title": f"{verb.title()} {description}",
        "module": module_name,
        "path": file_path,
        "language": lang,
        "lines": content.count("\n") + 1,
        "cliff_notes": [
            f"New {lang} module in {path_prefix.replace('/', '.')} for {domain.lower()}",
            f"Implements {description} ({ticket(rng)})",
            f"References {rng.randint(2, 5)} existing modules for cross-subsystem integration",
        ],
    }

    metadata = {
        "branch": f"feat/{module_name}-{slug}",
        "commit_msg": f"feat({module_name}): {verb} {description}",
        "pr_title": f"[{module_name}] {verb.title()} {description}",
        "pr_body": _code_pr_body(file_path, lang, description, summary, rng),
        "file_path": file_path,
    }

    return {
        "type": "code",
        "content": content,
        "summary": summary,
        "metadata": metadata,
        "files_to_commit": [(file_path, content)],
        "image_path": None,
    }


def _paper_pr_body(title, authors, summary, tr_num, rng):
    return f"""## Research Publication: TR-2026-{tr_num:03d}

**{title}**
*{authors}*

### Summary

{summary['cliff_notes'][0]}. {summary['cliff_notes'][1]}.

### Tracking

- Internal ref: {internal_doc(rng)}
- Related: {ticket(rng)}, {ticket(rng)}
- Review requested: {rng.choice(TEAM_MEMBERS)}

---
*Published via Souken Research Division automated pipeline.*
"""


def _rfc_pr_body(title, rfc_num, summary, rng):
    return f"""## RFC-{rfc_num:03d}: {title}

### Abstract

{summary['abstract'][:300]}...

### Key Points

- {summary['cliff_notes'][0]}
- {summary['cliff_notes'][1]}
- {summary['cliff_notes'][2]}

### Tracking

- Depends on: {ticket(rng)}, {ticket(rng)}
- Reviewed by: {rng.choice(TEAM_MEMBERS)}, {rng.choice(TEAM_MEMBERS)}

---
*RFC submitted via Souken Architecture Review Board.*
"""


def _code_pr_body(file_path, lang, description, summary, rng):
    return f"""## Feature: {description}

### Changes

- New `{lang}` module: `{file_path}`
- {summary['cliff_notes'][0]}
- {summary['cliff_notes'][1]}

### Testing

- Unit tests: pending ({ticket(rng)})
- Integration verified against staging environment

### Tracking

- {ticket(rng)}
- Reviewed by: {rng.choice(TEAM_MEMBERS)}

---
*Automated submission via Souken CI/CD pipeline v{fake_version(rng)}.*
"""


def ship_breakthrough(result, status_callback=None):
    """
    Ship a generated breakthrough: create branch, commit, push, PR, merge.
    status_callback(msg) is called with progress updates.
    Returns dict with success status and details.
    """
    def status(msg):
        if status_callback:
            status_callback(msg)
        print(msg)

    meta = result["metadata"]
    branch = meta["branch"]

    try:
        os.chdir(REPO_ROOT)

        # Ensure we're on master and up to date
        status("Syncing with master...")
        _run_git("checkout", "master")
        _run_git("pull", "--rebase", "origin", "master")

        # Create branch
        status(f"Creating branch: {branch}")
        _run_git("checkout", "-b", branch)

        # Write files
        status("Writing files...")
        for file_path, content in result["files_to_commit"]:
            abs_path = os.path.join(REPO_ROOT, file_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)

            if content is None and result.get("image_path"):
                # Binary file copy (image)
                shutil.copy2(result["image_path"], abs_path)
            elif content is not None:
                with open(abs_path, "w", encoding="utf-8") as f:
                    f.write(content)

        # Stage and commit
        status("Committing...")
        for file_path, _ in result["files_to_commit"]:
            _run_git("add", file_path)
        _run_git("commit", "-m", meta["commit_msg"])

        # Push
        status(f"Pushing to origin/{branch}...")
        _run_git("push", "-u", "origin", branch)

        # Create PR
        status("Creating pull request...")
        pr_url = _run_cmd(
            "gh", "pr", "create",
            "--title", meta["pr_title"],
            "--body", meta["pr_body"],
            "--base", "master",
            "--head", branch,
        )

        # Auto-merge
        status("Merging pull request...")
        _run_cmd("gh", "pr", "merge", "--merge", "--delete-branch")

        # Return to master
        status("Returning to master...")
        _run_git("checkout", "master")
        _run_git("pull", "--rebase", "origin", "master")

        # Save state
        state = load_state()
        state.update(result["state_update"])
        save_state(state)

        status(f"Breakthrough shipped! PR: {pr_url.strip()}")
        return {"success": True, "pr_url": pr_url.strip(), "branch": branch}

    except Exception as e:
        # Try to recover to master
        try:
            _run_git("checkout", "master")
        except Exception:
            pass
        status(f"ERROR: {e}")
        return {"success": False, "error": str(e)}


def _run_git(*args):
    """Run a git command in the repo root."""
    result = subprocess.run(
        ["git"] + list(args),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def _run_cmd(*args):
    """Run a shell command."""
    result = subprocess.run(
        list(args),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


if __name__ == "__main__":
    # CLI mode: generate and ship immediately
    state = load_state()
    result = generate_breakthrough(state)
    print(f"\n=== {result['type'].upper()} GENERATED ===")
    print(f"Title: {result['summary'].get('title', 'N/A')}")
    print(f"Branch: {result['metadata']['branch']}")
    print(f"File: {result['metadata']['file_path']}")
    print(f"\nCliff Notes:")
    for note in result['summary'].get('cliff_notes', []):
        print(f"  - {note}")
    print()

    resp = input("Ship it? [y/N] ").strip().lower()
    if resp == "y":
        ship_breakthrough(result)
    else:
        print("Aborted.")
