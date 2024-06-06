-- Question + answer chunks
WITH Questions AS (
    SELECT
        q.Id AS QuestionId,
        q.Body AS QuestionBody
    FROM
        Post q
    WHERE
        q.PostTypeId = 1
),
Answers AS (
    SELECT
        a.ParentId AS QuestionId,
        a.Body AS AnswerBody,
        a.Score AS AnswerScore
    FROM
        Post a
    WHERE
        a.PostTypeId = 2
),
Concatenated AS (
    SELECT
        q.QuestionId,
        q.QuestionBody || COALESCE('|' || STRING_AGG(a.AnswerBody, '|' ORDER BY a.AnswerScore DESC), '') AS question_and_answers
    FROM
        Questions q
    LEFT JOIN
        Answers a ON q.QuestionId = a.QuestionId
    GROUP BY
        q.QuestionId, q.QuestionBody
)
SELECT
    question_and_answers
FROM
    Concatenated
ORDER BY
    QuestionId;

