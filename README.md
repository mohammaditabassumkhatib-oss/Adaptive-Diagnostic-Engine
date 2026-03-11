# Adaptive Diagnostic Engine

A 1-Dimension Adaptive Testing system for GRE preparation, built with 
FastAPI, MongoDB, and OpenAI. The system dynamically adjusts question 
difficulty based on student performance using Item Response Theory (IRT).

---

## Tech Stack

- **Backend:** Python 3.11, FastAPI
- **Database:** MongoDB Atlas (via Motor async driver)
- **AI Integration:** OpenAI gpt-4o-mini
- **Algorithm:** 1D Item Response Theory (IRT)

---

## System Architecture

```
Student Client
      │
      │  HTTP Requests (REST API)
      ▼
┌─────────────────────┐
│  FastAPI Backend    │  ← Routes, validation, response formatting
│  (Uvicorn Server)   │
└─────────┬───────────┘
          │
          │  Answer submitted → trigger IRT update
          ▼
┌─────────────────────┐
│  Adaptive Engine    │  ← Pure Python, no external dependencies
│  (1PL IRT Algorithm)│    Updates θ, selects next difficulty target
└─────────┬───────────┘
          │
          │  Read questions / Write session state
          ▼
┌─────────────────────┐
│  MongoDB Atlas      │  ← Questions collection (indexed by difficulty+topic)
│  Questions + Session│    Sessions collection (tracks full answer history)
└─────────┬───────────┘
          │
          │  Only called once — when session completes (10 questions)
          ▼
┌─────────────────────┐
│  OpenAI GPT-4o-mini │  ← Receives session summary (topics, score, difficulty)
│  Study Plan Generator│   Returns personalized 3-step learning plan
└─────────────────────┘
```

### Data Flow Summary

1. Student hits `/session/start` → MongoDB creates a session with θ=0.5
2. Student hits `/next-question` → MongoDB finds closest unseen question to current θ
3. Student hits `/submit-answer` → IRT engine updates θ → MongoDB saves new state
4. Steps 2–3 repeat for 10 questions
5. Student hits `/study-plan` → summary sent to OpenAI → plan returned

### Key Design Decisions

- **Adaptive Engine is stateless** — it takes θ and difficulty as inputs, returns new θ.
  No database calls inside the engine, making it independently testable.
- **OpenAI is called only once per session** — not per question — keeping API costs minimal.
- **MongoDB aggregation handles question selection** — the `$abs` distance pipeline
  finds the closest difficulty question without loading all questions into memory.

---

## Getting Started

### Prerequisites
- Python 3.9+
- A MongoDB Atlas account (free tier is sufficient)
- An OpenAI API key

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/adaptive-diagnostic-engine.git
   cd adaptive-diagnostic-engine
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and fill in your values:
   ```
   MONGODB_URI=mongodb+srv://youruser:yourpass@cluster0.xxxxx.mongodb.net/
   DB_NAME=adaptive_db
   OPENAI_API_KEY=sk-...
   ```

4. Run the server
   ```bash
   uvicorn app.main:app --reload
   ```

5. The database seeds automatically on first startup.
   Open http://localhost:8000/docs for the interactive API explorer.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/session/start?student_id=xyz` | Start a new test session |
| GET | `/next-question?session_id=abc` | Get the next adaptive question |
| POST | `/submit-answer` | Submit an answer and update ability score |
| GET | `/study-plan?session_id=abc` | Get AI-generated study plan (after 10 questions) |

### Example Flow

**1. Start a session**
```bash
curl -X POST "http://localhost:8000/session/start?student_id=student_001"
```
```json
{ "session_id": "a3f9bc12", "ability_score": 0.5 }
```

**2. Get next question**
```bash
curl "http://localhost:8000/next-question?session_id=a3f9bc12"
```
```json
{
  "question_id": "q_003",
  "text": "If f(x) = x² - 4x + 4, for what value of x does f(x) = 0?",
  "options": {"A": "0", "B": "1", "C": "2", "D": "4"},
  "topic": "Algebra",
  "difficulty": 0.5
}
```

**3. Submit an answer**
```bash
curl -X POST "http://localhost:8000/submit-answer" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "a3f9bc12", "question_id": "q_003", "student_answer": "C"}'
```
```json
{
  "is_correct": true,
  "correct_answer": "C",
  "new_ability_score": 0.65,
  "questions_remaining": 9,
  "session_complete": false
}
```

**4. Get study plan (after all 10 questions)**
```bash
curl "http://localhost:8000/study-plan?session_id=a3f9bc12"
```

---

## Adaptive Algorithm Explained

The system uses a simplified **1-Parameter Item Response Theory (1PL IRT)** 
model to estimate student ability in real time.

### Core Concept

Every student has an **ability score θ (theta)**, initialized at 0.5. 
Every question has a **difficulty score b**, ranging from 0.1 to 1.0. 
After each answer, θ is updated based on whether the student's performance 
matched the statistical expectation.

### The Math

**Step 1 — Predict probability of a correct answer:**
```
P = 1 / (1 + e^(-(θ - b) × 1.7))
```

**Step 2 — Calculate the error (surprise):**
```
error = actual_result (1 or 0) - P
```

**Step 3 — Update ability score:**
```
θ_new = θ_old + 0.3 × error
```
Clamped between 0.1 and 1.0 to stay within question difficulty range.

### Why This Works

- If a strong student (θ=0.8) answers an easy question (b=0.2) correctly,
  P≈0.98 — expected, so θ barely moves.
- If a weak student (θ=0.3) answers a hard question (b=0.8) correctly,
  P≈0.08 — surprising, so θ jumps significantly upward.
- This means the score reacts more to *unexpected* results — exactly how
  a smart examiner would think.

### Question Selection

After each update, the next question is selected by finding the unseen 
question whose difficulty is **closest to the current θ**. This ensures 
the test always operates at the student's frontier — not too easy, 
not too hard.

### Key Parameters

| Parameter | Value | Reasoning |
|---|---|---|
| Initial θ | 0.5 | Neutral starting point, mid-range difficulty |
| Learning rate α | 0.3 | Balances responsiveness vs. stability over 10 questions |
| IRT scaling constant D | 1.7 | Standard psychometric constant |
| Test length | 10 questions | Enough for convergence, short enough for usability |

---

## AI Log: How AI Tools Were Used

### What AI helped with

**Claude (claude.ai)** was used as the primary architectural thinking 
partner throughout this project:

- Designed the MongoDB schema (Questions + UserSession collections),
  including the compound index strategy on `{difficulty, topic}` for 
  performant question lookup.
- Explained and derived the IRT update formula, including why α=0.3 
  is appropriate for a 10-question test window.
- Suggested the MongoDB aggregation pipeline for finding the 
  "closest difficulty" question — specifically the `$addFields` + 
  `$abs` + `$subtract` pattern, which I wasn't familiar with.
- Helped structure the project with clean separation of concerns 
  (routes → services → db layers).

**OpenAI gpt-4o-mini** is used at runtime to generate the personalized 
study plan. The prompt was manually crafted and tuned to produce 
structured 3-step output.

### What AI couldn't solve / required human judgment

- **Tuning α = 0.3:** AI suggested a range (0.2–0.4). I tested 
  values manually and chose 0.3 after observing that 0.4 caused 
  θ to swing too aggressively on the first 2-3 questions.
- **The duplicate question guard:** The `$nin` filter in the 
  aggregation pipeline needed to be manually verified — early 
  versions had a bug where seen questions could reappear after 
  session restore.
- **Prompt engineering for the study plan:** The first version 
  of the OpenAI prompt returned generic advice. I added 
  explicit fields (topics_struggled, peak_difficulty_reached) 
  to the prompt context to force specificity.
- **Async vs sync MongoDB client:** Motor (async) and PyMongo 
  (sync) have different APIs. AI occasionally generated PyMongo 
  syntax in async context — I had to catch and fix these manually.

---

## Project Structure

```
adaptive-diagnostic-engine/
├── app/
│   ├── main.py                 # FastAPI entry point + DB seeding
│   ├── api/routes.py           # HTTP endpoints
│   ├── services/
│   │   ├── adaptive_engine.py  # IRT algorithm
│   │   ├── session_service.py  # Core business logic
│   │   └── ai_service.py       # OpenAI study plan generation
│   ├── db/
│   │   ├── connection.py       # MongoDB client singleton
│   │   └── seed.py             # 20 GRE questions + index setup
│   └── models/schemas.py       # Pydantic request/response models
├── .env.example
├── requirements.txt
└── README.md
```

---

## Sample Output

At the end of a 10-question session, the system produces:

```json
{
  "summary": {
    "total_questions": 10,
    "total_correct": 7,
    "final_ability_score": 0.9021,
    "topics_struggled": ["Vocabulary"],
    "topics_strong": ["Algebra", "Statistics", "Geometry", "Arithmetic"],
    "peak_difficulty_reached": 0.95
  },
  "study_plan": "Step 1: ... Step 2: ... Step 3: ..."
}
```

> The system correctly identified Vocabulary as the weak area and 
> generated a targeted study plan despite the student scoring 70% overall 
> — demonstrating that topic-level granularity matters more than 
> raw score for personalized learning.
