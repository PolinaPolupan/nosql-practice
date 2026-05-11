from fastapi import FastAPI, Request
from uuid import uuid4, UUID
from datetime import datetime

from db import session, init_db

app = FastAPI()

init_db()


@app.get("/")
def home():
    return {"message": "Survey API"}


@app.post("/surveys")
async def create_survey(request: Request):

    body = await request.json()

    survey_id = uuid4()

    creator_id = UUID(body["creator_id"])

    created_at = datetime.utcnow()

    query1 = """
        INSERT INTO survey_by_id (
            survey_id,
            creator_id,
            title,
            description,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    query2 = """
        INSERT INTO surveys_by_creator (
            creator_id,
            created_at,
            survey_id,
            title,
            description
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    session.execute(
        query1,
        (
            survey_id,
            creator_id,
            body["title"],
            body["description"],
            created_at
        )
    )

    session.execute(
        query2,
        (
            creator_id,
            created_at,
            survey_id,
            body["title"],
            body["description"]
        )
    )

    return {
        "message": "Survey created",
        "survey_id": str(survey_id)
    }


@app.get("/surveys/{survey_id}")
def get_survey(survey_id: str):

    query = """
        SELECT * FROM survey_by_id
        WHERE survey_id = %s
    """

    result = session.execute(
        query,
        (UUID(survey_id),)
    )

    row = result.one()

    if not row:
        return {"error": "Survey not found"}

    return dict(row._asdict())


@app.get("/users/{creator_id}/surveys")
def get_user_surveys(creator_id: str):

    query = """
        SELECT * FROM surveys_by_creator
        WHERE creator_id = %s
    """

    result = session.execute(
        query,
        (UUID(creator_id),)
    )

    return [dict(row._asdict()) for row in result]


@app.put("/surveys/{survey_id}")
async def update_survey(
    survey_id: str,
    request: Request
):

    body = await request.json()

    query = """
        UPDATE survey_by_id
        SET title = %s,
            description = %s
        WHERE survey_id = %s
    """

    session.execute(
        query,
        (
            body["title"],
            body["description"],
            UUID(survey_id)
        )
    )

    return {"message": "Survey updated"}


@app.delete("/surveys/{survey_id}")
def delete_survey(survey_id: str):

    query = """
        DELETE FROM survey_by_id
        WHERE survey_id = %s
    """

    session.execute(
        query,
        (UUID(survey_id),)
    )

    return {"message": "Survey deleted"}


@app.post("/surveys/{survey_id}/questions")
async def add_question(
    survey_id: str,
    request: Request
):

    body = await request.json()

    question_id = uuid4()

    query = """
        INSERT INTO questions_by_survey (
            survey_id,
            question_order,
            question_id,
            question_text,
            question_type
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    session.execute(
        query,
        (
            UUID(survey_id),
            body["question_order"],
            question_id,
            body["question_text"],
            body["question_type"]
        )
    )

    return {
        "message": "Question added",
        "question_id": str(question_id)
    }


@app.get("/surveys/{survey_id}/questions")
def get_questions(survey_id: str):

    query = """
        SELECT * FROM questions_by_survey
        WHERE survey_id = %s
    """

    result = session.execute(
        query,
        (UUID(survey_id),)
    )

    return [dict(row._asdict()) for row in result]


@app.post("/surveys/{survey_id}/responses")
async def submit_response(
    survey_id: str,
    request: Request
):

    body = await request.json()

    response_id = uuid4()

    user_id = UUID(body["user_id"])

    submitted_at = datetime.utcnow()

    response_query = """
        INSERT INTO responses_by_survey (
            survey_id,
            submitted_at,
            response_id,
            user_id
        )
        VALUES (%s, %s, %s, %s)
    """

    session.execute(
        response_query,
        (
            UUID(survey_id),
            submitted_at,
            response_id,
            user_id
        )
    )

    for answer in body["answers"]:

        answer_query = """
            INSERT INTO answers_by_response (
                response_id,
                question_id,
                answer_text
            )
            VALUES (%s, %s, %s)
        """

        session.execute(
            answer_query,
            (
                response_id,
                UUID(answer["question_id"]),
                answer["answer_text"]
            )
        )

    return {
        "message": "Response submitted",
        "response_id": str(response_id)
    }


@app.get("/surveys/{survey_id}/responses")
def get_responses(survey_id: str):

    query = """
        SELECT * FROM responses_by_survey
        WHERE survey_id = %s
    """

    result = session.execute(
        query,
        (UUID(survey_id),)
    )

    return [dict(row._asdict()) for row in result]


@app.get("/responses/{response_id}/answers")
def get_answers(response_id: str):

    query = """
        SELECT * FROM answers_by_response
        WHERE response_id = %s
    """

    result = session.execute(
        query,
        (UUID(response_id),)
    )

    return [dict(row._asdict()) for row in result]