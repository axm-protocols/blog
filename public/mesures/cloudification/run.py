#!/usr/bin/env python3
"""Token-cost demo: agent-au-jugé (Read/Grep) vs agent-qui-appelle-l'outil (ast_search).

Same deterministic task on the same frozen corpus (axm-git @ git/v0.4.0):
    "List every function/method in this package that returns a ToolResult."

Arm A — the agent reads the code itself (tools: Read, Grep, Glob).
Arm B — the agent calls the deterministic tool (tools: Bash → `axm ast_search`).

We measure, per run: input/output/cache tokens, $ (computed from public Haiku
pricing, NOT the subscription SDK figure), num_tool_calls, duration, and
*correctness* against a known ground truth of 18 hits.

Run from the axm-cortex workspace venv:
    <axm-cortex-venv>/bin/python run.py
"""

from __future__ import annotations

import asyncio
import json
import re
import statistics
from dataclasses import asdict, dataclass
from pathlib import Path

from axm_harness.core.factory import get_adapter
from axm_harness.core.runner import run

# --- Fixed parameters -------------------------------------------------------

MODEL = "claude-haiku-4-5-20251001"
N_RUNS = 8
# axm-git frozen at tag git/v0.4.0 (== PyPI axm-git==0.4.0), cloned locally.
CORPUS = "<clone>/packages/axm-git"
# The `axm` CLI from an axm-forge venv (ships the ast_search tool).
AXM_BIN = "<axm-forge-venv>/bin/axm"

# Public Haiku 4.5 pricing (USD per 1M tokens) — used to convert tokens → $
# transparently, since auth_mode=subscription makes the SDK $ figure unreliable.
PRICE_IN_PER_MTOK = 1.00
PRICE_OUT_PER_MTOK = 5.00
PRICE_CACHE_READ_PER_MTOK = 0.10

# Ground truth: 18 functions/methods returning ToolResult (from ast_search).
# We score the agent's free-text answer by how many of these *distinctive*
# (non-`execute`) names it surfaces, plus how many `execute` methods it counts.
GROUND_TRUTH_DISTINCTIVE = [
    "timeout_error_result",
    "not_a_repo_error",
    "_validation_failure",
    "_validate_commit_spec",
    "_process_single_commit",
    "_check_dirty",
    "_preflight",
    "_list",
    "_add",
    "_remove",
]
GROUND_TRUTH_TOTAL = 18
GROUND_TRUTH_EXECUTE = 8  # 8 homonymous execute() methods across tool classes

PROMPT_A = (
    "You are working in the Python package at the current directory. "
    "You do NOT have any code-analysis tool — read the source yourself. "
    "List EVERY function and method in this package whose return type is "
    "`ToolResult` (including unions like `ToolResult | None`). For each, give "
    "its name and the file it lives in. Be exhaustive. End your answer with a "
    "line `TOTAL: <n>` giving the count."
)

PROMPT_B = (
    "You are working in the Python package at the current directory. "
    "A deterministic code-analysis CLI is available. To list every function "
    "whose return type is `ToolResult`, run exactly:\n"
    f"  {AXM_BIN} ast_search --path . --returns ToolResult\n"
    "Run it, then report the function names and files it found. End your answer "
    "with a line `TOTAL: <n>` giving the count."
)

ARMS = {
    "A_au_juge": {"prompt": PROMPT_A, "tools": ["Read", "Grep", "Glob"]},
    "B_outil": {"prompt": PROMPT_B, "tools": ["Bash"]},
}


@dataclass
class RunMetrics:
    arm: str
    idx: int
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    num_tool_calls: int
    num_turns: int
    duration_ms: int
    usd_computed: float
    found_distinctive: int  # of 10
    reported_total: int | None  # the TOTAL: <n> the agent claimed
    output_excerpt: str


def compute_usd(inp: int, out: int, cache: int) -> float:
    return (
        inp / 1_000_000 * PRICE_IN_PER_MTOK
        + out / 1_000_000 * PRICE_OUT_PER_MTOK
        + cache / 1_000_000 * PRICE_CACHE_READ_PER_MTOK
    )


def score_correctness(output: str) -> tuple[int, int | None]:
    """Count distinctive ground-truth names present + parse the claimed TOTAL."""
    found = sum(1 for name in GROUND_TRUTH_DISTINCTIVE if name in output)
    m = re.search(r"TOTAL:\s*(\d+)", output)
    reported = int(m.group(1)) if m else None
    return found, reported


async def run_one(arm: str, idx: int, adapter) -> RunMetrics:
    spec = ARMS[arm]
    r = await run(
        adapter,
        spec["prompt"],
        {
            "model": MODEL,
            "cwd": CORPUS,
            "tools": spec["tools"],
            "max_turns": 30,
        },
    )
    found, reported = score_correctness(r.output)
    return RunMetrics(
        arm=arm,
        idx=idx,
        input_tokens=r.total_input_tokens,
        output_tokens=r.total_output_tokens,
        cache_read_tokens=r.total_cache_read_tokens,
        num_tool_calls=r.num_tool_calls,
        num_turns=r.num_turns,
        duration_ms=r.duration_ms,
        usd_computed=compute_usd(
            r.total_input_tokens, r.total_output_tokens, r.total_cache_read_tokens
        ),
        found_distinctive=found,
        reported_total=reported,
        output_excerpt=r.output[:300],
    )


async def main() -> None:
    adapter = get_adapter("claude-agent-sdk", auth_mode="auto")
    print(f"auth: {adapter._resolved_auth} | model: {MODEL} | N={N_RUNS}")
    print(f"corpus: {CORPUS}")
    print(
        f"ground truth: {GROUND_TRUTH_TOTAL} hits "
        f"({len(GROUND_TRUTH_DISTINCTIVE)} distinctive + {GROUND_TRUTH_EXECUTE} execute)\n"
    )

    results: list[RunMetrics] = []
    for arm in ARMS:
        for idx in range(N_RUNS):
            print(f"  running {arm} #{idx + 1}/{N_RUNS} ...", flush=True)
            m = await run_one(arm, idx, adapter)
            results.append(m)
            print(
                f"    in={m.input_tokens} out={m.output_tokens} "
                f"cache={m.cache_read_tokens} calls={m.num_tool_calls} "
                f"found={m.found_distinctive}/10 total_claimed={m.reported_total} "
                f"${m.usd_computed:.5f}",
                flush=True,
            )

    # Persist raw metrics for the writeup.
    out_path = Path("<workdir>/metrics.json")
    out_path.write_text(json.dumps([asdict(m) for m in results], indent=2))
    print(f"\nraw metrics → {out_path}")

    # Aggregate per arm.
    print("\n=== AGGREGATE (mean over N runs) ===")
    for arm in ARMS:
        rs = [m for m in results if m.arm == arm]
        inp = [m.input_tokens for m in rs]
        out = [m.output_tokens for m in rs]
        calls = [m.num_tool_calls for m in rs]
        usd = [m.usd_computed for m in rs]
        found = [m.found_distinctive for m in rs]
        totals = [m.reported_total for m in rs]
        print(
            f"{arm}: in={statistics.mean(inp):.0f}±{(statistics.pstdev(inp)):.0f} "
            f"out={statistics.mean(out):.0f} calls={statistics.mean(calls):.1f} "
            f"${statistics.mean(usd):.5f} "
            f"found={statistics.mean(found):.1f}/10 totals_claimed={totals}"
        )


if __name__ == "__main__":
    asyncio.run(main())
