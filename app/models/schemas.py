from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    student_answer: str

class QuestionResponse(BaseModel):
    question_id: str
    text: str
    options: dict
    topic: str
    difficulty: float

class SessionResponse(BaseModel):
    session_id: str
    ability_score: float
    questions_answered: int

class AnswerFeedback(BaseModel):
    is_correct: bool
    correct_answer: str
    new_ability_score: float
    questions_remaining: int

class StudyPlan(BaseModel):
    final_ability_score: float
    topics_struggled: List[str]
    study_plan: str          # The LLM generated text