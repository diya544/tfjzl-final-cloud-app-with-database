from django.urls import path
from . import views

urlpatterns = [
    # List all courses
    path('', views.course_list, name='course_list'),

    # Show lesson + quiz
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),

    # REQUIRED FOR TASK 6 ✅
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # REQUIRED FOR TASK 6 ✅
    path(
        'course/<int:course_id>/submission/<int:submission_id>/result/',
        views.show_exam_result,
        name='show_exam_result'
    ),
]
