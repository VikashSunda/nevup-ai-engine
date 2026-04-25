# NevUp AI Trading Coach — System of AI Engine (Track 2)

NevUp AI Trading Coach is a stateful behavioral intelligence backend designed to analyze trader psychology across sessions, persist coaching memory, and generate evidence-backed contextual interventions. This submission was built for the NevUp Hiring Hackathon 2026 under Track 2: System of AI Engine.

The objective of this system is not to act as a generic chatbot, but to serve as a persistent behavioral reasoning engine that can ingest historical trading sessions, identify recurring psychological pathologies, store memory across sessions, retrieve relevant prior context before generating interventions, stream coaching messages in real time, and audit all cited historical references for factual validity.

---

## Core Features

### 1. Behavioral Profiling Engine
- Loads `nevup_seed_dataset.json`
- Parses all sessions and trades for each trader
- Detects recurring pathologies such as:
  - revenge_trading
  - overtrading
  - plan_non_adherence
  - session_tilt
  - time_of_day_bias
  - position_sizing_inconsistency
- Returns evidence-backed `tradeId` and `sessionId` citations for every behavioral claim

### 2. Persistent Memory Layer
- Implements the required NevUp memory contract endpoints
- Stores session summaries, behavioral metrics, pathology tags, and raw session records
- Uses SQLite persistence so memory survives docker restarts

### 3. Context Retrieval Engine
- Retrieves historically relevant prior sessions before generating interventions
- Returns both relevant stored summaries and pattern identifiers

### 4. Real-Time Coaching Stream
- Uses FastAPI SSE StreamingResponse
- Streams token-by-token coaching language instead of delayed static blob response

### 5. Anti-Hallucination Audit
- Parses all cited UUID session references from a coaching message
- Verifies whether each cited session actually exists in persistent memory
- Returns found / not-found status

### 6. Reproducible Evaluation Harness
- Runs all 10 NevUp seeded trader profiles through the profiler
- Compares predictions against ground truth pathology labels
- Produces precision, recall, and F1 score report using sklearn

---

## How To Run

1. Build and start the service

    docker compose up --build

2. Generate JWT token for testing

    python generate_token.py

3. Run evaluation harness

    python eval/evaluate.py

Application starts at: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

---

## Implemented API Endpoints

- GET /profile/{userId}
- PUT /memory/{userId}/sessions/{sessionId}
- GET /memory/{userId}/context?relevantTo={signal}
- GET /memory/{userId}/sessions/{sessionId}
- POST /session/events
- POST /audit

---

## Technical Stack

FastAPI, SQLite, SQLAlchemy, SSE StreamingResponse, Scikit-learn, Docker Compose
