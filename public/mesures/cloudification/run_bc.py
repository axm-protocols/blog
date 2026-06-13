#!/usr/bin/env python3
"""Arms B' (tool-pure) and C (bash/grep expert) — completes the 4-regime demo.

After N=8 of A (naive) and B (free agent + ast_search), two more regimes:

  B'  tool-pure   — ONE ast_search call, read the output, done. max_turns=2,
                    prompt forbids re-verification. This is "calling the
                    deterministic tool properly": you trust the output, you do
                    not re-judge it. The deterministic regime.
  C   bash-expert — full shell (grep/rg/awk/sed), NO ast_search. The skeptic's
                    "a good grep suffices". Scored on the 18 incl. 4 unions a
                    naive grep misses.

Both scored against the AST ground truth (ground_truth.json, 18 hits).
Appends to metrics.json; does NOT touch A/B. Run from the axm-cortex venv.
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

MODEL = "claude-haiku-4-5-20251001"
N_RUNS = 8
CORPUS = "<clone>/packages/axm-git"          # axm-git frozen at git/v0.4.0
AXM_BIN = "<axm-forge-venv>/bin/axm"          # the `axm` CLI (ships ast_search)
METRICS = Path("<workdir>/metrics.json")
GROUND_TRUTH = Path("<workdir>/ground_truth.json")

PRICE_IN_PER_MTOK = 1.00
PRICE_OUT_PER_MTOK = 5.00
PRICE_CACHE_READ_PER_MTOK = 0.10

GT = json.loads(GROUND_TRUTH.read_text())
GT_TOTAL = len(GT)  # 18
GT_DISTINCTIVE = sorted({h["name"] for h in GT if h["name"] != "execute"})
UNION_NAMES = sorted({h["name"] for h in GT if h["returns"] != "ToolResult"})

PROMPT_BPRIME = (
    "You are working in the Python package at the current directory. A "
    "deterministic code-analysis CLI is available and authoritative. To list "
    "every function whose return type is `ToolResult`, run EXACTLY this one "
    "command and trust its output completely:\n"
    f"  {AXM_BIN} ast_search --path . --returns ToolResult\n"
    "Do NOT verify it with grep or by reading files — the tool is exact. Report "
    "the hits it printed, then end with a line `TOTAL: <n>` (the number of hits "
    "the tool returned)."
)

PROMPT_C = (
    "You are working in the Python package at the current directory. You have a "
    "full shell: grep, rg (ripgrep), awk, sed, find, and pipes. Use them like an "
    "expert to answer quickly and exactly. List EVERY function and method whose "
    "return type is `ToolResult`, INCLUDING union types like `ToolResult | None` "
    "or `ToolResult | tuple[...]`. Combine commands however you see fit. For each "
    "hit give its name and file. End your answer with a line `TOTAL: <n>`."
)

ARMS = {
    # B': tool-pure — bounded to one tool call + answer, no re-verification.
    "Bprime_outil_pur": {"prompt": PROMPT_BPRIME, "tools": ["Bash"], "max_turns": 2},
    # C: bash/grep expert — full shell, no ast_search, more turns to combine cmds.
    "C_bash_expert": {"prompt": PROMPT_C, "tools": ["Bash"], "max_turns": 30},
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
    found_distinctive: int
    found_of_18: int
    found_unions: int
    reported_total: int | None
    output_excerpt: str


def compute_usd(inp: int, out: int, cache: int) -> float:
    return (
        inp / 1_000_000 * PRICE_IN_PER_MTOK
        + out / 1_000_000 * PRICE_OUT_PER_MTOK
        + cache / 1_000_000 * PRICE_CACHE_READ_PER_MTOK
    )


def score(output: str) -> tuple[int, int, int, int | None]:
    fd = sum(1 for n in GT_DISTINCTIVE if n in output)
    f18 = sum(1 for h in GT if h["name"] in output)
    fu = sum(1 for n in UNION_NAMES if n in output)
    m = re.search(r"TOTAL:\s*(\d+)", output)
    rep = int(m.group(1)) if m else None
    return fd, f18, fu, rep


async def run_one(arm: str, idx: int, adapter) -> RunMetrics:
    spec = ARMS[arm]
    try:
        r = await run(
            adapter,
            spec["prompt"],
            {
                "model": MODEL,
                "cwd": CORPUS,
                "tools": spec["tools"],
                "max_turns": spec["max_turns"],
            },
        )
    except Exception as exc:  # noqa: BLE001 — max-turns / SDK errors are a RESULT here
        # An arm that fails to converge within max_turns is a measurable outcome,
        # not a crash. Record it as an incomplete run (did_not_converge).
        return RunMetrics(
            arm=arm,
            idx=idx,
            input_tokens=-1,
            output_tokens=-1,
            cache_read_tokens=-1,
            num_tool_calls=-1,
            num_turns=-1,
            duration_ms=-1,
            usd_computed=-1.0,
            found_distinctive=-1,
            found_of_18=-1,
            found_unions=-1,
            reported_total=None,
            output_excerpt=f"DID_NOT_CONVERGE: {str(exc)[:200]}",
        )
    fd, f18, fu, rep = score(r.output)
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
        found_distinctive=fd,
        found_of_18=f18,
        found_unions=fu,
        reported_total=rep,
        output_excerpt=r.output[:400],
    )


async def main() -> None:
    adapter = get_adapter("claude-agent-sdk", auth_mode="auto")
    print(f"auth: {adapter._resolved_auth} | model: {MODEL} | N={N_RUNS} | ARMS B'+C")
    print(f"ground truth: {GT_TOTAL} hits | unions: {UNION_NAMES}\n")

    results: list[RunMetrics] = []
    for arm in ARMS:
        for idx in range(N_RUNS):
            print(f"  running {arm} #{idx + 1}/{N_RUNS} ...", flush=True)
            m = await run_one(arm, idx, adapter)
            results.append(m)
            # Incremental save after EVERY run — never lose data to a crash.
            existing = json.loads(METRICS.read_text()) if METRICS.exists() else []
            existing.append(asdict(m))
            METRICS.write_text(json.dumps(existing, indent=2))
            print(
                f"    in={m.input_tokens} out={m.output_tokens} cache={m.cache_read_tokens} "
                f"calls={m.num_tool_calls} of18={m.found_of_18}/18 unions={m.found_unions}/4 "
                f"total={m.reported_total} ${m.usd_computed:.5f}",
                flush=True,
            )
    print(f"\nsaved {len(results)} runs incrementally -> {METRICS}")

    print("\n=== AGGREGATE (mean over N runs) ===")
    for arm in ARMS:
        rs = [m for m in results if m.arm == arm]
        usd = [m.usd_computed for m in rs]
        f18 = [m.found_of_18 for m in rs]
        fu = [m.found_unions for m in rs]
        calls = [m.num_tool_calls for m in rs]
        totals = [m.reported_total for m in rs]
        print(
            f"{arm}: ${statistics.mean(usd):.5f}±{statistics.pstdev(usd):.5f} "
            f"calls={statistics.mean(calls):.1f} of18={statistics.mean(f18):.1f}/18 "
            f"unions={statistics.mean(fu):.1f}/4 totals={totals}"
        )


if __name__ == "__main__":
    asyncio.run(main())
