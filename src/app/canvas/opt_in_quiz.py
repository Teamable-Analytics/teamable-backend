from app.canvas.canvas_api import init_canvas
from app.models.course import Course
from app.models.organization import LMSTypeOptions


def create_opt_in_quiz_canvas(request, course: Course):
    if (
        course.organization is None
        or course.organization.lms_type != LMSTypeOptions.CANVAS
    ):
        return

    canvas = init_canvas(request, course.organization)
    canvas_course = canvas.get_course(course.lms_course_id)

    quiz = canvas_course.create_quiz(
        {
            "title": "Opt-in",
            "quiz_type": "survey",
        }
    )

    # "Yes" will be the correct answer meaning they have opted in
    quiz.create_question(
        question={
            "name": "Opt-in",
            "question_text": "Do you want to opt-in?",
            "question_type": "multiple_choice_question",
            "answers": [
                {
                    "answer_text": "Yes",
                    "answer_weight": 100,
                },
                {
                    "answer_text": "No",
                    "answer_weight": 0,
                },
            ],
        }
    )

    course.lms_opt_in_quiz_id = quiz.id
    course.save()
