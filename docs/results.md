# Results — all tables

Every number below is copied from the trial fact sheet, with its condition. Display values may be rounded for presentation (e.g. 3/592 ≈ 0.5%); the underlying fact sheet is not published with this cookbook, so the original precision versus display rounding cannot be checked here. No figure is rounded or merged across measurement conditions in the presentation of a single cell.

## Table 1 — Eleven-category medians

Measurement conditions: 2 runs per category; score = category mean ×100; median taken; spread >5 marked ⚠ and adjudicated on the lower run; t=0; tool-call parser = the model's official parser (`muse_glimmer`); reasoning set to `low` (cannot be disabled); the 200K tier of c2 was unservable at native 131072 ctx and recorded N/A, excluded from both sides of the mean.

| category | DeepSeek V4 Flash VE (baseline B) | 27B (reference) | solo Flash-Next (P1) | dual Flash-Next (P2) | **Muse low (P3)** |
|---|---|---|---|---|---|
| c1-kbqa | 86.7 | 100.0 | 95.0 | 95.0 | **98.3** |
| c2-longctx | 90.0 ⚠(86.7/93.3) | 65.0 | 100.0 | 98.3 | **63.3** |
| c3-tool | 73.3 ⚠(70.0/76.7) | 66.7 | 86.7 ⚠(83.3/90.0) | 88.3 | **53.3** |
| c4-code | 87.5 | 95.8 | 91.7 ⚠(87.5/95.8) | 91.7 ⚠(87.5/95.8) | **95.8** |
| c5-extract | 92.1 | 89.3 | 91.1 | 90.6 | **88.2** |
| c6-vision | 81.2 | 80.0 | 87.5 | 87.5 | **90.0** |
| c7-zhif | 78.3 | 86.7 | 85.0 | 85.0 | **80.0** |
| c7-agentic-if | 95.0 | 80.0 | 87.5 | 85.0 ⚠(80.0/90.0) | **79.2** |
| c8-judgment | 76.7 ⚠(73.3/80.0) | 89.2 | 70.8 | 70.0 | **76.7** |
| c9-long-coding | 99.3 | 97.2 | 97.6 | 97.2 | **75.0 ⚠(66.7/83.3)** |
| c10-sre-ops | 83.3 ⚠(80.0/86.7) | 90.0 | 88.3 | 90.0 | **93.3** |
| c2 (32K/95K, 20 questions; 200K tier N/A, excluded) | 92.5 [85.0, 100.0] ⚠ | 97.5 [100.0, 95.0] | 100.0 [100.0, 100.0] | 97.5 [95.0, 100.0] | **95.0 [95.0, 95.0]** |
| own mean (8 categories, original basis) | 87.3 | 88.0 | 92.0 | 91.9 | **85.5** |
| pack mean (3 categories) | 81.7 | 78.6 | 81.7 | 81.1 | **69.7** |
| errors / cat-runs | 1 / 22 | 20 / 22 | 0 / 22 | 0 / 22 | **23 / 22** |

Notes: c6 90.0 and c10 93.3 are the highest values across all five columns; c2's 63.3 reflects the 200K tier being unservable at native 131072 ctx, the 20-question 32K/95K figure is 95.0 [95.0, 95.0]; c9 median 75.0 with runs 66.7/83.3, adjudicated 66.7. The comparison columns (27B reference, solo/dual Flash-Next P1/P2, baseline B) are named by role; their full model revisions, precisions, images, launch flags and sampling/inference configs are not recorded, so the comparison is not rebuildable as a fair match from this cookbook alone. The own/pack category membership and weighting are not recorded; the `own mean` and `pack mean` rows are reproduced from the trial's own basis, which is not published here.

## Table 2 — Speed, KV pool, boot

Measurement conditions: K1 protocol; boot = time to first real (non-empty) generation request, not `/health`; reasoning `low`.

| metric | DeepSeek V4 Flash VE (B) | 27B (ref) | solo Flash-Next (P1) | dual Flash-Next (P2) | **Muse low (P3)** |
|---|---|---|---|---|---|
| decode tok/s | 31.8 | 20.0 | 36.6 | 52.9 | **27.1** |
| cold prefill tok/s | 2085 | 1957 | 2144 | 2989 | **2822** |
| 6-stream aggregate tok/s | 81.2 | 88.0 | 56.6 | 91.8 | **116.1** |
| KV tokens @ `max_model_len` | 1,301,037 @ 1,048,320 | — | 1,134,794 @ 262,144 | 3,042,386 @ 262,144 | **2,817,481 @ 131,072** |
| boot s | — | — | 300 | 300 | **520** |

Notes: KV figures across different ctx configurations are only comparable against absolute gates, not against each other (different `max_model_len` per column). The 6-stream aggregate 116.1 is the highest of the five columns. Boot 520 s (real request) vs the inventory/community figure 371 s (371–411 s) — both listed, different measurements.

## Table 3 — Median wall clock per category, seconds

Measurement conditions: runner-recorded; parallel 4; reasoning `low`.

| category | DeepSeek V4 Flash VE (B) | 27B (ref) | solo Flash-Next (P1) | dual Flash-Next (P2) | **Muse low (P3)** |
|---|---|---|---|---|---|
| c1-kbqa | 19 | 36 | 41 | 28 | **60** |
| c2-longctx | 1288 | 752 | 1594 | 1177 | **563** |
| c3-tool | 39 | 66 | 68 | 118 | **137** |
| c4-code | 10 | 85 | 19 | 12 | **75** |
| c5-extract | 42 | 52 | 51 | 34 | **142** |
| c6-vision | 18 | 19 | 22 | 179 | **145** |
| c7-zhif | 24 | 16 | 23 | 14 | **92** |
| c7-agentic-if | 43 | 70 | 78 | 210 | **254** |
| c8-judgment | 69 | 63 | 107 | 72 | **268** |
| c9-long-coding | 839 | 131 | 180 | 178 | **1033** |
| c10-sre-ops | 32 | 60 | 54 | 34 | **94** |

Notes: the Muse wall-clock gate compares against the 27B reference (≤3×): c3-tool 137 s vs 66 s = ×2.1 ✓; c7-zhif 92 s vs 16 s = ×5.8 ✗; c10-sre-ops 94 s vs 60 s = ×1.6 ✓. The recorded wall-clock column holds per-category medians, not per-question ratios, and the per-category ratios against the baseline column vary widely across categories, so a single 2.5–4× per-question range is not supported by the recorded numbers.

## Table 4 — Gate-by-gate adjudication (frozen rules v2), Muse low (P3) vs the baseline

Measurement conditions: frozen adjudication rules v2, applied in order (stability → key categories → other categories → performance gates → Δown tie zone → Muse-specific wall-clock gate); baseline B = DeepSeek V4 Flash Vision-Exp (the comparison baseline; no production-system identity is attached).

| gate | value vs threshold | result |
|---|---|---|
| stability | errors 23 (cat-runs 22), with the c2 200K tier recorded N/A (over-native-ctx) rather than error; records true errors 3/592 = **0.5%** (gate ≤1%); boot 520 s | reported with both counts (see "What did not work") |
| key c3-tool | 53.3 vs B 70.0 (gate ≥65.0) | ✗ |
| key c4-code | 95.8 vs B 87.5 (gate ≥82.5) | ✓ |
| key c8-judgment | 76.7 vs B 73.3 (gate ≥68.3) | ✓ |
| key c9-long-coding | 66.7 vs B 99.3 (gate ≥94.3) | ✗ |
| c1-kbqa | 98.3 vs 86.7 (gate ≥76.7) | ✓ |
| c2-longctx | 95.0 vs B 85.0 (adjudicated low; 92.5 [85.0, 100.0], spread 15 >5) (gate ≥75.0) | ✓ |
| c5-extract | 88.2 vs 92.1 (gate ≥82.1) | ✓ |
| c6-vision | 90.0 vs 81.2 (gate ≥71.2) | ✓ |
| c7-zhif | 80.0 vs 78.3 (gate ≥68.3) | ✓ |
| c7-agentic-if | 79.2 vs 95.0 (gate ≥85.0) | ✗ |
| c10-sre-ops | 93.3 vs 80.0 (gate ≥70.0) | ✓ |
| decode | 27.1 (gate ≥30) | ✗ |
| prefill | 2822 (gate ≥1000) | ✓ |
| 6-stream | 116.1 (gate ≥60) | ✓ |
| KV | 2,817,481 (gate ≥1,000,000) | ✓ |
| Δown (common categories, c2 on the 20-question basis) | 88.4 − 87.2 = **+1.2** → tie zone | tie zone, not a win |
| Δown reproducibility note | own/pack category membership, weights and the averaging formula are **not recorded**; 88.4 / 87.2 cannot be rebuilt from the category table here, and applying the spread>5 low-run rule to c2 (B 85.0) and c9 (P3 66.7) would change the Δown value — the corrected value is not recorded. Tie-zone numeric bounds (boundary, inclusivity of equality, rule version) are not recorded, so the +1.2 → tie-zone classification is taken from the trial's own verdict. The tie-zone "KV ≥ B" condition is read against each column's absolute KV gate, not as a cross-configuration comparison (KV across different `max_model_len` is not comparable). | not recorded |
| Muse wall-clock gate | c7-zhif ×5.8 (92 s vs 16 s; 92÷16=5.75→5.8) (gate ≤3×) | ✗ |
| conclusion | negative result; production unchanged | |

## Table 5 — Diagnostic breakdown of the c3 failure

Measurement conditions: single-run breakdown, from the records.

| dimension | score |
|---|---|
| Tool Selection | 1/3 |
| Multi-Step | 2/5 |
| Restraint | 2/2 |
| Error Recovery | 2/3 |

Note: weakness is in tool selection and multi-step chains, not in restraint. This single-run breakdown does not reconstruct the two-round c3 median of 53.3; the run, weights and the second-round scores behind it are not recorded, so the diagnostic is not traceable back to the c3 total.

## Reference — community / inventory numbers (not our trial measurements)

Measurement conditions: Dell Pro Max with GB10 deployability inventory, 2026-09-17, before the trial; partly vendor-reported. These are **not** reproduced by the trial and are listed only as context that was carried into the plan. The in-repo original text, versions and test conditions behind these figures are not recorded, so they cannot be independently verified from this cookbook.

| Item | Value | Source basis |
|---|---|---|
| Decode without draft | **11.7 tok/s** | inventory / classmethod figures |
| Decode with DFlash | **21.6 tok/s** | inventory / classmethod figures |
| Decode on SGLang + DFlash | **23.7 tok/s** | inventory (SGLang NVFP4 build observed has **no vision weights** → vision categories score 0; speed reference only; specific build / weight manifest not recorded) |
| KV pool | **4.82M tokens** (no draft) / **3.58M** (with draft); ≈2.25× the Qwen3.6-27B pool of **2.14M** with no draft (4.82/2.14), ≈1.67× with draft (3.58/2.14) | inventory |
| 8-way concurrent aggregate | **159 tok/s** | inventory |
| Boot | **371 s** (compile + autotune + graph); range **371–411 s** in the recipe notes | inventory |
| Draft speed-up claim | "6 patches, 25→57 tok/s" (community forum claim) | third-party claim, **not reproduced by us** |
| Vendor/analyst scores | MCP Atlas **75.5**; τ3-Banking **23.5** (beats Qwen3.6-27B); loses SWE-V / TerminalBench; independent AA index **35** vs Qwen3.6-27B **38**; hallucination rate **82%** | inventory (third-party tables) |
