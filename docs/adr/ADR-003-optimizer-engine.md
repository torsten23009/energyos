# ADR-003: Optimizer strategy
**Status: Accepted for alpha / future choice pending** — 2026-10-24

Decision: Ship a simple deterministic read-only surplus advisor now. Define an adapter boundary for future HAEO, EMHASS and EOS comparison. No dependency on cloud LLM, dynamic optimization solver or heavy worker on Pi 4 until benchmarked.

Alternative considered: immediately bundle a large solver stack. Rejected pending HAOS/Pi compatibility and performance testing.
