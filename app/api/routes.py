from fastapi import APIRouter, HTTPException
from app.models.schemas import SubmitAnswerRequest
from app.services import session_service, ai_service

router = APIRouter()

@router.post("/session/start")
async def start_session(student_id: str):
    session = await session_service.create_session(student_id)
    return {"session_id": session["session_id"], "ability_score": 0.5}


@router.get("/next-question")
async def next_question(session_id: str):
    question = await session_service.get_next_question(session_id)
    if not question:
        raise HTTPException(status_code=404, detail="No question found or session complete")
    return {
        "question_id": question["question_id"],
        "text": question["text"],
        "options": question["options"],
        "topic": question["topic"],
        "difficulty": question["difficulty"]
    }


@router.post("/submit-answer")
async def submit_answer(body: SubmitAnswerRequest):
    result = await session_service.process_answer(
        body.session_id,
        body.question_id,
        body.student_answer
    )
    return result


@router.get("/study-plan")
async def get_study_plan(session_id: str):
    from app.db.connection import get_database
    db = get_database()
    session = await db["sessions"].find_one({"session_id": session_id})

    if not session or session["status"] != "completed":
        raise HTTPException(status_code=400, detail="Session not complete yet")

    plan = await ai_service.generate_study_plan(session["summary"])
    return {"study_plan": plan, "summary": session["summary"]}