from answers.models import Question,Answer

FIELD_INDEXES = {
    Question: {'indexed': ['topic', 'content']},
    Answer: {'indexed': ['content']},
}