<script>
  // Interactive island: the measured 2×2 of the cassation experiment.
  // Hover a cell to read its rate; toggle which gate is shown to feel the
  // orthogonality — the witness lights the SCOPE column, the judge the
  // CORRECTNESS row. Self-contained (no d3 in the template); the grid is
  // precomputed reactively so SSR and hydration render the same thing.

  export let labels = { fr: {}, en: {} };
  export let lang = 'fr';

  const L = (k) => (labels[lang] && labels[lang][k]) || (labels.fr && labels.fr[k]) || k;

  // Real numbers from the population-axis run (see BILAN_2X2.md).
  // rate[gate][scope][correctness]
  const RATES = {
    witness: { over: { correct: 0.87, incorrect: 0.87 }, well: { correct: 0.10, incorrect: 0.10 } },
    judge:   { over: { correct: 0.00, incorrect: 1.00 }, well: { correct: 0.00, incorrect: 1.00 } },
  };

  const COLS = ['correct', 'incorrect'];   // x axis: correctness
  const ROWS = ['over', 'well'];           // y axis: scope overflow

  let gate = 'witness';
  let hover = null;

  // warm ramp #f3efe9 -> #8a5a2b, computed in plain JS (no dependency)
  function ramp(v) {
    const t = Math.max(0, Math.min(1, v));
    const a = [243, 239, 233], b = [138, 90, 43];
    const c = a.map((x, i) => Math.round(x + (b[i] - x) * t));
    return `rgb(${c[0]},${c[1]},${c[2]})`;
  }

  // Precompute every cell so the template is a simple loop (robust under SSR).
  $: grid = ROWS.map((scope) =>
    COLS.map((corr) => {
      const v = RATES[gate][scope][corr];
      return { scope, corr, v, bg: ramp(v), fg: v > 0.5 ? '#fff' : '#1a1a1a' };
    })
  );
</script>

<figure class="viz">
  <div class="controls">
    <button class:on={gate === 'witness'} on:click={() => (gate = 'witness')}>{L('witness')}</button>
    <button class:on={gate === 'judge'} on:click={() => (gate = 'judge')}>{L('judge')}</button>
  </div>

  <div class="grid" role="img" aria-label={L('aria')}>
    <div class="corner"></div>
    {#each COLS as c}<div class="colhead">{L(c)}</div>{/each}

    {#each grid as row, ri}
      <div class="rowhead">{L(ROWS[ri])}</div>
      {#each row as cell}
        <div
          class="cell"
          style="background:{cell.bg}; color:{cell.fg}"
          on:mouseenter={() => (hover = cell)}
          on:mouseleave={() => (hover = null)}
          on:focus={() => (hover = cell)}
          on:blur={() => (hover = null)}
          role="button"
          tabindex="0"
        >
          {cell.v.toFixed(2)}
        </div>
      {/each}
    {/each}
  </div>

  <figcaption>
    {#if hover}
      <strong>{Math.round(hover.v * 100)}%</strong> — {L(gate)} · {L(hover.scope)} / {L(hover.corr)}
    {:else}
      {gate === 'witness' ? L('cap_witness') : L('cap_judge')}
    {/if}
  </figcaption>
</figure>

<style>
  .viz { margin: 2rem 0; font-family: 'Inter', system-ui, sans-serif; }
  .controls { display: flex; gap: 0.5rem; margin-bottom: 0.9rem; }
  .controls button {
    font: inherit; font-size: 0.85rem; padding: 0.3rem 0.85rem; cursor: pointer;
    background: transparent; border: 1px solid var(--rule, #e6e3dd); border-radius: 999px;
    color: var(--ink-soft, #555); transition: all 0.12s ease;
  }
  .controls button.on { background: var(--ink, #1a1a1a); color: var(--ground, #faf9f7); border-color: var(--ink, #1a1a1a); }
  .grid { display: grid; grid-template-columns: 6.5rem 1fr 1fr; gap: 5px; max-width: 27rem; }
  .colhead, .rowhead { font-size: 0.78rem; color: var(--ink-soft, #555); display: flex; align-items: center; }
  .colhead { justify-content: center; padding-bottom: 0.25rem; }
  .rowhead { justify-content: flex-end; padding-right: 0.65rem; text-align: right; }
  .cell {
    aspect-ratio: 16 / 9; display: flex; align-items: center; justify-content: center;
    font-weight: 600; font-size: 1.15rem; border-radius: 6px; cursor: pointer;
    transition: transform 0.12s ease; font-variant-numeric: tabular-nums;
  }
  .cell:hover, .cell:focus { transform: scale(1.05); outline: none; }
  figcaption { margin-top: 0.9rem; font-size: 0.85rem; color: var(--ink-soft, #555); min-height: 1.4em; }
</style>
