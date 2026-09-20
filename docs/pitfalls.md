# Pitfalls

Each pitfall is expanded with **symptom / root cause / fix / how we found it**, in the order encountered.

## 1. Tool calls truncated mid-call

- **Symptom:** tool calls are cut off in the middle of a call; output stops at the `<|eom|>` token.
- **Root cause:** the launch was missing `--generation-config auto`, so the model's tool-call output format was not applied and generation was truncated at the end-of-message token (observed on this deployment; the image/flag version, a request example, the `generation_config`, and a before/after output are not recorded, so the fix is not independently verified here).
- **Fix:** always pass `--generation-config auto`.
- **How we found it:** tool-call requests returned incomplete tool invocations during the c3-tool runs; adding `--generation-config auto` to the launch flags resolved the truncation. The condition (flag required) is recorded in the launch-flags table.

## 2. Thinking still verbose with reasoning set to low

- **Symptom:** with `Reasoning strength: low` in the system prompt, the model still emits 5–10× the tokens of the comparison baseline (per-question token counts, the corresponding baseline, the counting range and the output ceiling are not recorded, so the multiple is a recorded observation, not verifiable from this cookbook); three c9 questions hit the 900 s per-question budget with 21–26K-token outputs.
- **Root cause:** reasoning on this deployment **cannot** be turned off — the settings are `low/medium/high/xhigh` with no `off`. `low` only reduces, it does not disable (a model config / version proving "no off" is not recorded, so this is an observation of this deployment, not a general property of all same-named builds).
- **Fix:** no fix. Report per-question wall clock and token counts alongside scores, and treat non-disableable reasoning as a deployment-surface limitation that inflates wall clock and timeout exposure.
- **How we found it:** the wall-clock column showed inflation relative to the baseline even after setting reasoning to low; the c9 900 s timeouts with 21–26K-token outputs supported the output-length-inflation observation (the recorded wall-clock column holds per-category medians, not a uniform 2.5–4× per-question ratio; see the wall-clock-table notes).

## 3. `tool_choice: required` returns 0 tool calls silently

- **Symptom:** requests sent with `tool_choice: required` return 0 tool calls, with no error surfaced to the client.
- **Root cause:** vLLM behavior on this model — `required` does not force a tool call here (vLLM revision, the tools/schema, parser/request params and the raw response are not recorded; the root cause restates the symptom, and only the zero-call symptom was detected, so `required` semantics are not confirmed fixed, only detected).
- **Fix:** do not rely on `tool_choice: required`; validate actual tool-call counts in the harness and treat a zero-call response as a failure.
- **How we found it:** c3-tool runs where the harness set `required` returned zero tool calls without an error; the harness call-count check flagged it. Recorded in the launch-flags / eval-condition notes.

## 4. All 200K-tier long-context questions fail

- **Symptom:** all ten 200K-tier c2 questions (IDs in the 020–029 range) fail on run 1 with `errors=10`; the raw c2 score falls to 63.3.
- **Root cause:** native `max_position_embeddings` is 131072 with no `rope_scaling`; `--max-model-len 131072` is already the native ceiling, so the 200K tier cannot be served at all.
- **Fix:** record the 200K tier as **N/A** and exclude it from both sides of the mean (never score it 0). Keep the separate 20-question 32K/95K figure (95.0 [95.0, 95.0] for this model).
- **How we found it:** run 1 of c2 returned `errors=10` for the 200K-tier questions; the model card / config showed `max_position_embeddings` 131072 and no `rope_scaling`, confirming the ceiling. The common-category exclusion rule was then applied.

## 5. Three c9 questions hit the 900 s per-question budget

- **Symptom:** three c9-long-coding questions reach the 900 s per-question timeout budget with outputs of 21–26K tokens; c9 records runs of 66.7/83.3 (adjudicated 66.7, gate ≥94.3, a failed gate).
- **Root cause:** non-disableable reasoning (see pitfall 2) inflates output length, so long-coding questions run far past the time budget before producing an answer (hypothesis; the frozen-budget failure result under the 900 s cap is kept, but a relaxed-budget correctness retest or paired control is not recorded, so a coding-ability failure is not excluded).
- **Fix:** budget per-question timeouts against reasoning-inflated outputs **before** comparing wall clock across models; do not attribute the timeout to a model-quality gap when it is driven by reasoning verbosity.
- **How we found it:** the c9 wall-clock column (1033 s median) and the recorded 900 s timeouts with 21–26K-token outputs pointed at reasoning-inflated length as a hypothesis, not a proven coding-ability verdict.

## 6. Vision categories all 0 on the SGLang speed build

- **Symptom:** on the SGLang NVFP4 build, all vision categories score 0.
- **Root cause:** the SGLang NVFP4 build observed here ships **no vision weights**, so the ViT-G/14 1.8B tower is absent and vision questions cannot be answered (recorded from the inventory note; the specific weights, build version and manifest are not recorded, and a vision-0 result from this trial is not recorded, so it is not generalised to all same-named builds).
- **Fix:** use the vLLM NVFP4 build for any quality run involving vision; use SGLang only as a speed reference. For a vision cross-check only, use llama.cpp + mmproj (3/3 correct, 15 s startup — not reproducible: no llama.cpp commit, GGUF/mmproj file, launch command or three test inputs are recorded, so the 3/3 / 15 s claim is not independently verifiable).
- **How we found it:** the inventory note for the SGLang decode figure (23.7 tok/s) explicitly states the build has no vision weights → vision categories score 0; this disqualified the SGLang lane for quality work.

## 7. "25→57 tok/s with DFlash" doesn't match our decode

- **Symptom:** the community/forum claim "6 patches, 25→57 tok/s with DFlash" does not match our K1 decode measurement of 27.1 tok/s, and the model fails the decode gate (≥30).
- **Root cause:** the claim is a community/forum figure from different patches and a different stack (the six patches and the community's original config are not recorded, so the performance gap is not confirmed caused by those factors — only that the experiments differ); the inventory DFlash figure is 21.6 tok/s, our K1 protocol run measured 27.1 tok/s — three different measurements under three different conditions.
- **Fix:** never carry community speed numbers into gates; re-measure with the K1 protocol on the exact stack being adjudicated.
- **How we found it:** the trial's own K1 decode (27.1) sat below both the community claim and the gate; the fact sheet lists the claim explicitly as "third-party claim, not reproduced by us."

## 8. KV pools look comparable across configurations

- **Symptom:** KV-token counts across columns (2,817,481 @ 131,072; 1,134,794 @ 262,144; 3,042,386 @ 262,144; 1,301,037 @ 1,048,320) look directly comparable but are not.
- **Root cause:** each column ran at a different `max_model_len` (the four columns span three distinct values — 131072, 262144, 1048320 — since both Flash-Next columns are 262144), so the KV pool size is a function of the configured context. No same-model run varying only `max_model_len` is recorded, and the other columns' model/precision/memory config is not fully recorded, so the capacity difference is not directly attributable to `max_model_len` alone; only the "not directly comparable" point is supported.
- **Fix:** compare KV tokens only against absolute gates (here ≥1,000,000), and record `max_model_len` alongside every KV number.
- **How we found it:** the KV row of the speed table spans three distinct `max_model_len` values across four columns (131072 / 262144 / 1048320; two columns share 262144); the condition note under the table states they are only comparable against absolute gates, not against each other.

## 9. No recipe exists for this model in the community cluster stack

- **Symptom:** there is no Muse recipe in the community cluster stack, so the usual recipe-driven launch path does not apply.
- **Root cause:** recipe gap — the model is not covered by the existing recipe set (the community cluster stack repo, version and recipe list are not recorded, so the scope and time-point of "no recipe" are not verified).
- **Fix:** launch solo with an explicit image tag via the private switch script's solo mode (behaviour: stop the running stack container, pull the trial image, launch with the flags; public abstraction `switch/stack-mode.sh` in the sibling repo dell-pro-max-gb10-vllm-stack-ab; inspection `docker logs --tail 4000 <container>`, removal `docker rm -f <container>`), or use a bare `docker run`. The full launch command is not recorded in the sources, so the launch step is described, not copy-pasteable.
- **How we found it:** the launch-route row of the launch-flags table records that no Muse recipe exists and that the solo-mode / bare-`docker run` path was used instead.

## 10. First real request takes far longer than "started"

- **Symptom:** the engine reports "started" (and `/health` returns 200) well before it can actually serve, so readiness declared on `/health` would be premature.
- **Root cause:** boot here is defined as the first true non-empty generation request (520 s in the trial), not `/health` — this is a timing definition, not a proven root cause. The inventory/community figure of 371 s (371–411 s) is a different measurement and cannot by itself prove `/health` reported ready early in this run.
- **Fix:** gate readiness on a real generation request with non-empty output, not on `/health`; log boot seconds in the evidence set.
- **How we found it:** the trial declared readiness only on a real generation request and recorded boot as 520 s. The same-launch `/health`=200 timestamp and the first-successful-generation timestamp are not recorded, so the "far too early" claim is not independently supported — only that readiness was gated on a real request and boot was 520 s.
