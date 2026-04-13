# W2 — Cache Breaker

## What is it?

Dynamic or unstable content placed early in the prompt.

Examples:
- timestamps
- request IDs
- session IDs

## Why it matters

Modern LLM providers support prompt caching.

If the prefix changes:
👉 cache is invalidated

Result:
- higher cost
- slower responses

## Example

### Bad

System message includes:
- current time
- unique request ID

### Better

- keep prefix static
- move dynamic content to the end

## Estimated impact

Typical savings:
**40% – 80%**

Especially in repeated workflows.

## Detection in this repo

- regex detection of dynamic patterns
- analysis of early messages

---
