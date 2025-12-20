from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson, Question, Choice
from django.http import HttpResponse


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.question_set.all()

    if request.method == "POST":
        total_marks = sum(q.grade for q in questions)
        score = 0
        results = []

        for question in questions:
            selected_choice_id = request.POST.get(str(question.id))

            correct_choices = question.choice_set.filter(is_correct=True)
            correct_answers = [c.choice_text for c in correct_choices]

            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                is_correct = selected_choice.is_correct

                if is_correct:
                    score += question.grade

                results.append({
                    "question": question.question_text,
                    "selected": selected_choice.choice_text,
                    "correct": correct_answers,
                    "is_correct": is_correct
                })
            else:
                results.append({
                    "question": question.question_text,
                    "selected": "Not answered",
                    "correct": correct_answers,
                    "is_correct": False
                })

        passed = score >= (0.5 * total_marks)

        return render(request, "course/quiz_result.html", {
            "lesson": lesson,
            "score": score,
            "total": total_marks,
            "passed": passed,
            "results": results
        })

    return render(request, "course/lesson_detail.html", {
        "lesson": lesson,
        "questions": questions
    })


def course_list(request):
    courses = Course.objects.all().distinct()
    return render(request, "course/course_list.html", {"courses": courses})


def submit(request, course_id):
    return HttpResponse("Submit view placeholder for Task 6")


def show_exam_result(request, course_id, submission_id):
    return HttpResponse("Exam result placeholder")
