from app.db.connection import get_database

questions = [
    # ── ALGEBRA (Easy → Hard) ──────────────────────────────
    {
        "question_id": "q_001",
        "text": "If 2x + 3 = 11, what is x?",
        "options": {"A": "2", "B": "3", "C": "4", "D": "5"},
        "correct_answer": "C",
        "difficulty": 0.1,
        "topic": "Algebra",
        "tags": ["linear_equations", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_002",
        "text": "What is the slope of the line passing through (1,2) and (3,8)?",
        "options": {"A": "2", "B": "3", "C": "4", "D": "6"},
        "correct_answer": "B",
        "difficulty": 0.3,
        "topic": "Algebra",
        "tags": ["slope", "coordinate_geometry", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_003",
        "text": "If f(x) = x² - 4x + 4, for what value of x does f(x) = 0?",
        "options": {"A": "0", "B": "1", "C": "2", "D": "4"},
        "correct_answer": "C",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["quadratic", "factoring", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_004",
        "text": "If |2x - 6| > 10, which of the following could be x?",
        "options": {"A": "0", "B": "3", "C": "6", "D": "9"},
        "correct_answer": "D",
        "difficulty": 0.7,
        "topic": "Algebra",
        "tags": ["absolute_value", "inequalities", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_005",
        "text": "For all real x, if f(x+1) = x² + 2x, what is f(x)?",
        "options": {"A": "x²", "B": "x²-1", "C": "x²+1", "D": "(x-1)²"},
        "correct_answer": "B",
        "difficulty": 0.9,
        "topic": "Algebra",
        "tags": ["function_substitution", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },

    # ── GEOMETRY (Easy → Hard) ─────────────────────────────
    {
        "question_id": "q_006",
        "text": "What is the area of a circle with radius 5?",
        "options": {"A": "10π", "B": "25π", "C": "50π", "D": "5π"},
        "correct_answer": "B",
        "difficulty": 0.15,
        "topic": "Geometry",
        "tags": ["circles", "area", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_007",
        "text": "A rectangle has perimeter 40 and width 8. What is its area?",
        "options": {"A": "96", "B": "192", "C": "48", "D": "112"},
        "correct_answer": "A",
        "difficulty": 0.35,
        "topic": "Geometry",
        "tags": ["rectangles", "perimeter", "area", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_008",
        "text": "In triangle ABC, angle A = 55°, angle B = 75°. What is angle C?",
        "options": {"A": "40°", "B": "50°", "C": "60°", "D": "70°"},
        "correct_answer": "B",
        "difficulty": 0.25,
        "topic": "Geometry",
        "tags": ["triangles", "angles", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_009",
        "text": "A cylinder has radius 3 and height 10. What is its volume?",
        "options": {"A": "30π", "B": "60π", "C": "90π", "D": "9π"},
        "correct_answer": "C",
        "difficulty": 0.55,
        "topic": "Geometry",
        "tags": ["cylinder", "volume", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_010",
        "text": "Two similar triangles have sides in ratio 3:5. What is the ratio of their areas?",
        "options": {"A": "3:5", "B": "6:10", "C": "9:25", "D": "27:125"},
        "correct_answer": "C",
        "difficulty": 0.75,
        "topic": "Geometry",
        "tags": ["similar_triangles", "area_ratio", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },

    # ── VOCABULARY (Easy → Hard) ───────────────────────────
    {
        "question_id": "q_011",
        "text": "Choose the word most similar in meaning to BENEVOLENT:",
        "options": {"A": "Cruel", "B": "Kind", "C": "Angry", "D": "Lazy"},
        "correct_answer": "B",
        "difficulty": 0.1,
        "topic": "Vocabulary",
        "tags": ["synonyms", "GRE_verbal"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_012",
        "text": "Choose the word most opposite in meaning to LOQUACIOUS:",
        "options": {"A": "Talkative", "B": "Reserved", "C": "Verbose", "D": "Cheerful"},
        "correct_answer": "B",
        "difficulty": 0.4,
        "topic": "Vocabulary",
        "tags": ["antonyms", "GRE_verbal"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_013",
        "text": "The professor's ______ remarks confused the students who expected clarity.",
        "options": {"A": "lucid", "B": "abstruse", "C": "simple", "D": "concise"},
        "correct_answer": "B",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["sentence_completion", "GRE_verbal"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_014",
        "text": "Choose the word most similar in meaning to OBSEQUIOUS:",
        "options": {"A": "Defiant", "B": "Fawning", "C": "Indifferent", "D": "Hostile"},
        "correct_answer": "B",
        "difficulty": 0.8,
        "topic": "Vocabulary",
        "tags": ["synonyms", "advanced", "GRE_verbal"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_015",
        "text": "The critic's ______ review was notable for its ______ of the director's previous acclaimed work.\nA) sycophantic… dismissal  B) trenchant… adulation  C) caustic… encomium  D) laudatory… censure",
        "options": {"A": "sycophantic/dismissal", "B": "trenchant/adulation", "C": "caustic/encomium", "D": "laudatory/censure"},
        "correct_answer": "C",
        "difficulty": 0.95,
        "topic": "Vocabulary",
        "tags": ["double_blank", "advanced", "GRE_verbal"],
        "times_attempted": 0,
        "times_correct": 0
    },

    # ── ARITHMETIC & NUMBER THEORY ─────────────────────────
    {
        "question_id": "q_016",
        "text": "What is 15% of 240?",
        "options": {"A": "36", "B": "48", "C": "24", "D": "30"},
        "correct_answer": "A",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["percentages", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_017",
        "text": "If a train travels 120 miles in 90 minutes, what is its speed in miles per hour?",
        "options": {"A": "70", "B": "80", "C": "90", "D": "100"},
        "correct_answer": "B",
        "difficulty": 0.4,
        "topic": "Arithmetic",
        "tags": ["speed_distance_time", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_018",
        "text": "What is the largest prime factor of 360?",
        "options": {"A": "2", "B": "3", "C": "5", "D": "7"},
        "correct_answer": "C",
        "difficulty": 0.6,
        "topic": "Arithmetic",
        "tags": ["prime_factors", "number_theory", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },

    # ── STATISTICS ─────────────────────────────────────────
    {
        "question_id": "q_019",
        "text": "A set of 5 numbers has a mean of 10. If four of the numbers are 8, 12, 9, and 11, what is the fifth?",
        "options": {"A": "8", "B": "9", "C": "10", "D": "12"},
        "correct_answer": "C",
        "difficulty": 0.45,
        "topic": "Statistics",
        "tags": ["mean", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
    {
        "question_id": "q_020",
        "text": "In a normal distribution, approximately what percentage of values fall within 2 standard deviations of the mean?",
        "options": {"A": "68%", "B": "90%", "C": "95%", "D": "99%"},
        "correct_answer": "C",
        "difficulty": 0.65,
        "topic": "Statistics",
        "tags": ["normal_distribution", "standard_deviation", "GRE_quant"],
        "times_attempted": 0,
        "times_correct": 0
    },
]


async def seed_questions():
    db = get_database()
    collection = db["questions"]

    # Avoid duplicate seeding on re-runs
    existing = await collection.count_documents({})
    if existing >= 20:
        print("✅ Questions already seeded. Skipping.")
        return

    await collection.insert_many(questions)

    # Create the index we designed in Step 1
    await collection.create_index([("difficulty", 1), ("topic", 1)])

    print(f"✅ Seeded {len(questions)} questions with index on difficulty + topic.")