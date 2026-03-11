import uuid
from datetime import datetime
from app.db.connection import get_database
from app.services.adaptive_engine import IRTAdaptiveEngine

TOTAL_QUESTIONS = 10

async def create_session(student_id: str) -> dict:
    db = get_database()
    session = {
        "session_id": str(uuid.uuid4())[:8],
        "student_id": student_id,
        "started_at": datetime.utcnow(),
        "ended_at": None,
        "status": "active",
        "ability_score": 0.5,
        "current_difficulty_target": 0.5,
        "questions_answered": [],
        "summary": None
    }
    await db["sessions"].insert_one(session)
    return session


async def get_next_question(session_id: str) -> dict | None:
    db = get_database()
    session = await db["sessions"].find_one({"session_id": session_id})

    if not session or session["status"] != "active":
        return None

    seen_ids = [q["question_id"] for q in session["questions_answered"]]
    target = session["current_difficulty_target"]

    # Find closest unseen question to target difficulty
    pipeline = [
        {"$match": {"question_id": {"$nin": seen_ids}}},
        {"$addFields": {
            "diff_distance": {
                "$abs": {"$subtract": ["$difficulty", target]}
            }
        }},
        {"$sort": {"diff_distance": 1}},
        {"$limit": 1}
    ]

    results = await db["questions"].aggregate(pipeline).to_list(length=1)
    return results[0] if results else None


async def process_answer(session_id: str, question_id: str, student_answer: str) -> dict:
    db = get_database()
    session = await db["sessions"].find_one({"session_id": session_id})
    question = await db["questions"].find_one({"question_id": question_id})

    is_correct = student_answer.upper() == question["correct_answer"].upper()

    # Run IRT update
    engine = IRTAdaptiveEngine(initial_ability=session["ability_score"])
    new_theta = engine.update_ability(question["difficulty"], is_correct)

    # Build answer record
    answer_record = {
        "question_id": question_id,
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "student_answer": student_answer,
        "is_correct": is_correct,
        "ability_score_before": session["ability_score"],
        "ability_score_after": new_theta,
        "answered_at": datetime.utcnow()
    }

    updated_answers = session["questions_answered"] + [answer_record]
    questions_remaining = TOTAL_QUESTIONS - len(updated_answers)
    is_finished = questions_remaining == 0

    # Build update payload
    update_data = {
        "ability_score": new_theta,
        "current_difficulty_target": engine.next_difficulty_target(),
        "questions_answered": updated_answers,
    }

    if is_finished:
        update_data["status"] = "completed"
        update_data["ended_at"] = datetime.utcnow()
        update_data["summary"] = build_summary(updated_answers, new_theta)

    await db["sessions"].update_one(
        {"session_id": session_id},
        {"$set": update_data}
    )

    return {
        "is_correct": is_correct,
        "correct_answer": question["correct_answer"],
        "new_ability_score": new_theta,
        "questions_remaining": questions_remaining,
        "session_complete": is_finished,
        "summary": update_data.get("summary")
    }


def build_summary(answers: list, final_theta: float) -> dict:
    topic_stats = {}

    for a in answers:
        t = a["topic"]
        if t not in topic_stats:
            topic_stats[t] = {"correct": 0, "total": 0}
        topic_stats[t]["total"] += 1
        if a["is_correct"]:
            topic_stats[t]["correct"] += 1

    struggled = [t for t, s in topic_stats.items() if s["correct"] / s["total"] < 0.5]
    strong = [t for t, s in topic_stats.items() if s["correct"] / s["total"] >= 0.5]

    return {
        "total_questions": len(answers),
        "total_correct": sum(1 for a in answers if a["is_correct"]),
        "final_ability_score": final_theta,
        "topics_struggled": struggled,
        "topics_strong": strong,
        "peak_difficulty_reached": max(a["difficulty"] for a in answers)
    }