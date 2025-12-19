from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Question, Choice, Submission
from django.contrib.auth.decorators import login_required

@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    # Create a new submission for this user and course
    submission = Submission.objects.create(user=user, course=course)
    
    # Get the POST data for selected choices
    selected_choice_ids = []
    for key in request.POST:
        if key.startswith('choice'):
            selected_choice_ids.append(int(request.POST[key]))

    # Add selected choices to the submission
    selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
    submission.choices.set(selected_choices)

    # Calculate score
    score = 0
    questions = Question.objects.filter(lesson__course=course)
    for question in questions:
        correct_choices = question.choice_set.filter(is_correct=True)
        if set(correct_choices) == set(selected_choices.filter(question=question)):
            score += question.grade

    submission.score = score
    submission.save()

    return redirect('show_exam_result', submission_id=submission.id)

@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choices = submission.choices.all()
    questions = Question.objects.filter(lesson__course=submission.course)

    context = {
        'submission': submission,
        'selected_choices': selected_choices,
        'questions': questions,
    }

    return render(request, 'exam_result.html', context)
