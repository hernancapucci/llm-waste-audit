# Methodology

`llm-waste-audit` v0.1 uses simple, transparent heuristics to detect two initial waste classes:

- **W1 — Context Bloat**
- **W2 — Cache Breaker**

## Scores

- **Cacheability Score**: 0–100, higher is better
- **Context Bloat Score**: 0–100, higher is worse

## Current detection logic

### W2 — Cache Breaker
Flags:
- timestamps or dates early in the prompt
- request IDs or session IDs in early prompt positions
- long or numerous tool definitions that may vary between requests

### W1 — Context Bloat
Flags:
- very large estimated context
- repeated context blocks
- long or numerous tool definitions

## Important note

This tool does **not** provide exact cost measurement in v0.1.

It provides:
- pattern detection
- approximate scoring
- estimated savings ranges
- concrete suggestions

## Principles

1. Reproducibility over hype
2. Transparent heuristics over fake precision
3. Incremental improvement over premature complexity
