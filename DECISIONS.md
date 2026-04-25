## Decision 1 — FastAPI selected as the serving framework

The NevUp AI Engine requires low-latency asynchronous endpoint handling, native server-sent event streaming, and lightweight production-grade API exposure. FastAPI was selected because it provides efficient async request execution, first-class `StreamingResponse` support for SSE coaching, automatic request validation, and built-in interactive API documentation while keeping the service minimal.

This directly supports NevUp's requirement for warm repeated coaching calls with low perceived latency.

---

## Decision 2 — SQLite chosen for persistent behavioral memory

NevUp explicitly disqualifies non-persistent in-memory memory stores that reset after docker restarts. To satisfy this, SQLite was selected as a lightweight local disk-backed persistence layer.

SQLite provides:
- restart-safe durability,
- simple local reproducibility,
- zero external database setup,
- queryable storage for summaries, metrics, tags, and raw records.

This keeps reviewer startup friction minimal while still satisfying the memory persistence requirement.

---

## Decision 3 — Deterministic pathology inference over opaque LLM-only classification

The provided seed dataset already contains strongly repetitive structural behavioral signatures across traders, including revenge flags, clustered overtrading bursts, emotional instability streaks, and quantity inconsistencies.

A deterministic evidence-backed pathology profiler was therefore preferred over black-box LLM-only classification because deterministic heuristics allow:

- reproducible outputs,
- exact tradeId/sessionId evidence citations,
- explainable pathology reasoning,
- elimination of unsupported generic hallucinations.

Since NevUp explicitly penalizes unsupported coaching claims, explainability was prioritized over purely linguistic generation.

---

## Decision 4 — SSE selected for streaming coaching delivery

NevUp requires coaching interventions to stream token-by-token rather than returning as a delayed static response.

Server Sent Events were chosen because:

- one-way server push is sufficient,
- implementation is simpler than WebSockets,
- browser/curl testing is straightforward,
- lower infrastructure complexity under hackathon constraints.

This allows the user to begin receiving coaching almost immediately while the rest of the intervention continues rendering.

---

## Decision 5 — Raw session payloads stored alongside summaries

A summary-only memory layer would not satisfy NevUp's hallucination audit requirement.

Therefore each persisted memory object stores:

- human-readable summary,
- behavioral metrics,
- pathology tags,
- full raw session JSON.

This ensures the system can both retrieve semantic prior context and perform factual verification whenever a coaching response cites a prior session.

---

## Decision 6 — Separate sklearn evaluation harness included

NevUp reviewers require a reproducible pathology classification report across all 10 seeded traders.

A standalone evaluation script was therefore created that:

1. loads ground truth pathology labels,
2. runs every trader through the same profiler,
3. compares predictions,
4. exports precision, recall, and F1 metrics.

This makes reviewer reruns transparent and independent of runtime API behavior.

---

## Decision 7 — Single-command Dockerized startup preserved

The hackathon packet explicitly requires the full submission to start with one `docker compose up` command and no manual environment setup.

For this reason:

- all dependencies are captured in `requirements.txt`,
- FastAPI bootstraps automatically,
- SQLite initializes internally,
- no external services are required.

This minimizes reviewer setup friction and maximizes reproducible execution reliability.