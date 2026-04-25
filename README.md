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
- Stores:
  - session summaries
  - behavioral metrics
  - pathology tags
  - raw session records
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

## Project Structure

nevup-ai-engine/
│
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── profiler.py
│   ├── memory_engine.py
│   ├── coaching.py
│   ├── audit.py
│   └── utils.py
│
├── data/
│   └── nevup_seed_dataset.json
│
├── eval/
│   └── evaluate.py
│
├── reports/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── generate_token.py
├── README.md
├── DECISIONS.md
└── .gitignore

---

## How To Run

### 1. Build and start the service

docker compose up --build

Application starts at:
http://localhost:8000

Swagger API docs:
http://localhost:8000/docs

### 2. Generate JWT token for testing

python generate_token.py

### 3. Run evaluation harness

python eval/evaluate.py

Generated evaluation report:
reports/classification_report.json

---

## Implemented API Endpoints

### GET /profile/{userId}
Returns structured pathology profile with evidence citations.

### PUT /memory/{userId}/sessions/{sessionId}
Stores persistent session memory summary.

### GET /memory/{userId}/context?relevantTo={signal}
Retrieves relevant historical memory context.

### GET /memory/{userId}/sessions/{sessionId}
Returns raw stored session record for audit verification.

### POST /session/events
Streams token-by-token contextual coaching intervention.

### POST /audit
Verifies all session references present in a coaching response.

---

## Authentication

All endpoints use NevUp's shared JWT HS256 signing secret.

Authorization header format:
Bearer <jwt_token>

Cross-tenant mismatch returns FORBIDDEN.

---

## Technical Stack

- FastAPI
- SQLite
- SQLAlchemy
- SSE StreamingResponse
- Scikit-learn
- Docker / Docker Compose

---

## Sample CURL Tests

Get Profile:
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/profile/f412f236-4edc-47a2-8f54-8763a6ed2ce8

Persist Memory:
curl -X PUT "http://localhost:8000/memory/f412f236-4edc-47a2-8f54-8763a6ed2ce8/4f39c2ea-8687-41f7-85a0-1fafd3e976df" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d "{\"summary\":\"Repeated revenge entries after losses\",\"metrics\":{\"risk\":\"high\"},\"tags\":[\"revenge_trading\"]}"

Fetch Context:
curl -H "Authorization: Bearer YOUR_TOKEN" "http://localhost:8000/memory/f412f236-4edc-47a2-8f54-8763a6ed2ce8/context?relevantTo=revenge_trading"

Streaming Coaching:
curl -N -X POST "http://localhost:8000/session/events" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d "{\"userId\":\"f412f236-4edc-47a2-8f54-8763a6ed2ce8\"}"

Audit:
curl -X POST "http://localhost:8000/audit" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d "{\"userId\":\"f412f236-4edc-47a2-8f54-8763a6ed2ce8\",\"coachingText\":\"Pattern repeated in session 4f39c2ea-8687-41f7-85a0-1fafd3e976df\"}"

---

## Submission Notes

This implementation was intentionally designed as an evidence-backed deterministic behavioral intelligence engine instead of a generic LLM-only chatbot in order to:

- eliminate hallucinated unsupported trader references,
- guarantee reproducible pathology detection,
- preserve memory across restarts,
- expose auditable reasoning traces,
- and satisfy NevUp's persistent AI infrastructure requirement.

The entire stack starts with a single:

docker compose up --build

as required by the hackathon packet.
