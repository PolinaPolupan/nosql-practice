CREATE KEYSPACE IF NOT EXISTS survey_app
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE survey_app;

CREATE TABLE IF NOT EXISTS survey_by_id (
    survey_id UUID PRIMARY KEY,
    creator_id UUID,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS surveys_by_creator (
    creator_id UUID,
    created_at TIMESTAMP,
    survey_id UUID,
    title TEXT,
    description TEXT,

    PRIMARY KEY (creator_id, created_at)
)
WITH CLUSTERING ORDER BY (created_at DESC);

CREATE TABLE IF NOT EXISTS questions_by_survey (
    survey_id UUID,
    question_order INT,
    question_id UUID,
    question_text TEXT,
    question_type TEXT,

    PRIMARY KEY (survey_id, question_order)
);

CREATE TABLE IF NOT EXISTS responses_by_survey (
    survey_id UUID,
    submitted_at TIMESTAMP,
    response_id UUID,
    user_id UUID,

    PRIMARY KEY (survey_id, submitted_at)
)
WITH CLUSTERING ORDER BY (submitted_at DESC);

CREATE TABLE IF NOT EXISTS answers_by_response (
    response_id UUID,
    question_id UUID,
    answer_text TEXT,

    PRIMARY KEY (response_id, question_id)
);


SELECT *
FROM survey_by_id
WHERE survey_id = 11111111-1111-1111-1111-111111111111;

SELECT *
FROM surveys_by_creator
WHERE creator_id = aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa;

SELECT *
FROM questions_by_survey
WHERE survey_id = 11111111-1111-1111-1111-111111111111;

SELECT *
FROM responses_by_survey
WHERE survey_id = 11111111-1111-1111-1111-111111111111;

SELECT *
FROM answers_by_response
WHERE response_id = ffffffff-ffff-ffff-ffff-ffffffffffff
AND question_id = cccccccc-cccc-cccc-cccc-cccccccccccc;