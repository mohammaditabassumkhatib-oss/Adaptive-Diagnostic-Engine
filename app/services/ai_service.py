from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_study_plan(summary: dict) -> str:

    prompt = f"""
    A student just completed an adaptive GRE diagnostic test. Here are their results:

    - Final Ability Score: {summary['final_ability_score']} (scale 0.1 to 1.0)
    - Total Questions: {summary['total_questions']}
    - Total Correct: {summary['total_correct']}
    - Topics They Struggled With: {', '.join(summary['topics_struggled']) or 'None'}
    - Topics They Did Well In: {', '.join(summary['topics_strong']) or 'None'}
    - Peak Difficulty Reached: {summary['peak_difficulty_reached']}

    Create a concise 3-step personalized study plan targeting their weak areas.
    Be specific, actionable, and encouraging. Each step should be 2-3 sentences.
    Format as Step 1, Step 2, Step 3.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7
    )

    return response.choices[0].message.content