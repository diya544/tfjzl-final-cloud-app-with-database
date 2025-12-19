from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),  # new homepage
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
]
