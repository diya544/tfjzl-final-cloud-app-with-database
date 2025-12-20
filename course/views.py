from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Question, Choice, Submission


def course_list(request):
    courses = Course.objects.all().distinct()
    return render(request, "course/course_list.html", {"courses": courses})


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.question_set.all()

    return render(request, "course/lesson_detail.html", {
        "lesson": lesson,
        "questions": questions
    })


# ✅ REQUIRED FOR TASK 5
@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # create submission
    submission = Submission.objects.create(
        user=request.user,
        course=course
    )

    # save selected choices
    for key, value in request.POST.items():
        if key.isdigit():
            choice = get_object_or_404(Choice, id=int(value))
            submission.choices.add(choice)

    return redirect(
        'show_exam_result',
        course_id=course.id,
        submission_id=submission.id
    )


# ✅ REQUIRED FOR TASK 5
@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)
    submission = get_object_or_404(Submission, id=submission_id)

    questions = Question.objects.filter(lesson__course=course)

    total_marks = sum(q.grade for q in questions)
    score = 0

    for question in questions:
        selected = submission.choices.filter(question=question)
        if selected.exists() and selected.first().is_correct:
            score += question.grade

    passed = score >= (0.5 * total_marks)

    return render(request, "course/exam_result_bootstrap.html", {
        "course": course,
        "submission": submission,
        "questions": questions,
        "score": score,
        "total_marks": total_marks,
        "passed": passed,
    })
