from cassandra.cluster import Cluster
from uuid import UUID
import time

time.sleep(15)

cluster = Cluster(["127.0.0.1"])

session = cluster.connect()

KEYSPACE = "survey_app"


def init_db():

    with open("schema.cql", "r") as file:
        schema = file.read()

    commands = schema.split(";")

    for command in commands:

        command = command.strip()

        if command:
            session.execute(command)

    session.set_keyspace(KEYSPACE)

    survey1_id = UUID("11111111-1111-1111-1111-111111111111")

    creator1_id = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

    session.execute(
        """
        INSERT INTO survey_by_id (
            survey_id,
            creator_id,
            title,
            description,
            created_at
        )
        VALUES (%s, %s, %s, %s, toTimestamp(now()))
        """,
        (
            survey1_id,
            creator1_id,
            "Programming Languages Survey",
            "Survey about programming languages"
        )
    )

    session.execute(
        """
        INSERT INTO surveys_by_creator (
            creator_id,
            created_at,
            survey_id,
            title,
            description
        )
        VALUES (%s, toTimestamp(now()), %s, %s, %s)
        """,
        (
            creator1_id,
            survey1_id,
            "Programming Languages Survey",
            "Survey about programming languages"
        )
    )

    survey2_id = UUID("22222222-2222-2222-2222-222222222222")

    creator2_id = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

    session.execute(
        """
        INSERT INTO survey_by_id (
            survey_id,
            creator_id,
            title,
            description,
            created_at
        )
        VALUES (%s, %s, %s, %s, toTimestamp(now()))
        """,
        (
            survey2_id,
            creator2_id,
            "Gaming Survey",
            "Survey about games"
        )
    )

    session.execute(
        """
        INSERT INTO surveys_by_creator (
            creator_id,
            created_at,
            survey_id,
            title,
            description
        )
        VALUES (%s, toTimestamp(now()), %s, %s, %s)
        """,
        (
            creator2_id,
            survey2_id,
            "Gaming Survey",
            "Survey about games"
        )
    )

    question1_id = UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")

    session.execute(
        """
        INSERT INTO questions_by_survey (
            survey_id,
            question_order,
            question_id,
            question_text,
            question_type
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            survey1_id,
            1,
            question1_id,
            "What language do you use most?",
            "text"
        )
    )

    question2_id = UUID("dddddddd-dddd-dddd-dddd-dddddddddddd")

    session.execute(
        """
        INSERT INTO questions_by_survey (
            survey_id,
            question_order,
            question_id,
            question_text,
            question_type
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            survey1_id,
            2,
            question2_id,
            "How many years of experience do you have?",
            "number"
        )
    )

    question3_id = UUID("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee")

    session.execute(
        """
        INSERT INTO questions_by_survey (
            survey_id,
            question_order,
            question_id,
            question_text,
            question_type
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            survey2_id,
            1,
            question3_id,
            "Favorite game genre?",
            "text"
        )
    )

    response1_id = UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")

    user1_id = UUID("99999999-9999-9999-9999-999999999999")

    session.execute(
        """
        INSERT INTO responses_by_survey (
            survey_id,
            submitted_at,
            response_id,
            user_id
        )
        VALUES (%s, toTimestamp(now()), %s, %s)
        """,
        (
            survey1_id,
            response1_id,
            user1_id
        )
    )

    response2_id = UUID("88888888-8888-8888-8888-888888888888")

    user2_id = UUID("77777777-7777-7777-7777-777777777777")

    session.execute(
        """
        INSERT INTO responses_by_survey (
            survey_id,
            submitted_at,
            response_id,
            user_id
        )
        VALUES (%s, toTimestamp(now()), %s, %s)
        """,
        (
            survey2_id,
            response2_id,
            user2_id
        )
    )

    session.execute(
        """
        INSERT INTO answers_by_response (
            response_id,
            question_id,
            answer_text
        )
        VALUES (%s, %s, %s)
        """,
        (
            response1_id,
            question1_id,
            "Python"
        )
    )

    session.execute(
        """
        INSERT INTO answers_by_response (
            response_id,
            question_id,
            answer_text
        )
        VALUES (%s, %s, %s)
        """,
        (
            response1_id,
            question2_id,
            "3"
        )
    )

    session.execute(
        """
        INSERT INTO answers_by_response (
            response_id,
            question_id,
            answer_text
        )
        VALUES (%s, %s, %s)
        """,
        (
            response2_id,
            question3_id,
            "RPG"
        )
    )

    print("Database initialized with test data")