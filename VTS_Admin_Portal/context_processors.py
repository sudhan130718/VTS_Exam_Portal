from exam.models import Exam
from .models import Course, Trainer

def developer_list(request):
    developers = Trainer.objects.filter(user__role='developer', is_active=True)
    developer_count = developers.count()  

    trainers = Trainer.objects.all()
    trainers_count = trainers.count() 

    course = Course.objects.all()
    course_count = course.count()  

    
    exam = Exam.objects.all()
    exam_count = exam.count()  



    return {
        'all_developers': developers,
        'developer_count': developer_count,
        'trainers_count': trainers_count,
        'course_count': course_count,
         'exam_count': exam_count,

    }


from datetime import datetime

def global_greeting(request):
    now = datetime.now()

    # Dynamic greeting
    if now.hour < 12:
        greeting = "Good Morning"
    elif now.hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return {
        'greeting': greeting,
        'today': now
    }

