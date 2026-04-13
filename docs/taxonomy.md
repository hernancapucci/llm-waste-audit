# Waste Taxonomy

## W1 — Context Bloat
Sending more context than necessary, especially when large static or low-relevance blocks are resent repeatedly.

## W2 — Cache Breaker
Dynamic or unstable content placed early in the prompt/request structure, reducing or eliminating cache reuse opportunities.

## W3 — Redundant Reasoning
Multiple reasoning steps or agents reproduce nearly identical work without meaningful gain.

## W4 — Model Overkill
Using a more expensive model than needed for a task’s complexity or reliability target.

## W5 — Output Excess
Requesting or allowing outputs much longer than required.

## W6 — Retrieval Waste
Retrieval systems returning too much, too little, or the wrong context at high token cost.

## W7 — Session Memory Failure
Lack of summarization or memory compression across sessions, forcing repeated full-context restarts.

## W8 — Unsafe Semantic Reuse
Cost-saving reuse strategies that may introduce semantic drift, stale answers, or poisoned reuse paths.
