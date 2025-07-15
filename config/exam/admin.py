from django.contrib import admin

from exam.models import Exam, ExamQuestion, TraineeAnswer, TraineeExam
from exam.models import  PracticalQuestion, PracticalAnswer

# Register your models here.
admin.site.register(ExamQuestion)
admin.site.register(Exam)
admin.site.register(TraineeExam)
admin.site.register(TraineeAnswer)



admin.site.register(PracticalQuestion)
admin.site.register(PracticalAnswer)
