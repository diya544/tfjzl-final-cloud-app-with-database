from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission, Instructor, Learner

# Inline classes
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

# Admin classes
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class OnlineCourseAdmin(admin.AdminSite):
    site_header = "OnlineCourse Administration"
    site_title = "OnlineCourse Admin"
    index_title = "Admin Dashboard"

# Register models
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor)
admin.site.register(Learner)
