from django.shortcuts import render,get_object_or_404

from VTS_Admin_Portal.models import Course, Trainee, Trainer
from exam.models import Exam, TraineeExam
from django.db.models import Q
# Create your views here.


def developer_dashboard(request):
     trainer = get_object_or_404(Trainer, user=request.user)
     return render(request, 'VTS_Developer_Portal/developer_dashboard.html', {'trainer': trainer })



def developer_trainee_card_view(request):
    try:
        trainer = Trainer.objects.get(user=request.user)
        trainees = Trainee.objects.filter(assigned_trainer=trainer)
    except Trainer.DoesNotExist:
        trainees = Trainee.objects.none()

    class_mode = request.GET.get('class_mode')  # can be 'online', 'offline', or None

    if class_mode:
        trainees = trainees.filter(class_mode__iexact=class_mode)

    return render(request, 'VTS_Developer_Portal/developer_trainee_card_view.html', {
        'trainees': trainees,
        'selected_mode': class_mode
    })







    





def developer_exam(request):
    trainer = Trainer.objects.get(user=request.user) 
    courses = Course.objects.filter(trainer=trainer)
    print('courses', courses)

    exams = Exam.objects.filter(course__in=courses).order_by('-id')

    return render(request, 'VTS_Developer_Portal/developer_exam.html', {'exams': exams})

def developer_result(request):
    role = request.GET.get('role')
    trainer = Trainer.objects.get(user=request.user)  
    trainee = Trainee.objects.filter(assigned_trainer=trainer)  
    results = TraineeExam.objects.filter(trainee__in=trainee).order_by('-submitted_at')
    search_exam = request.GET.get('e', '')  

    if role:
            results = TraineeExam.objects.filter(exam__title=role).order_by('-submitted_at') 

     
    if search_exam:
     results = results.filter(
    Q(trainee__user__full_name__icontains=search_exam) |
    Q(submitted_at__icontains=search_exam) 
    
     )        




    return render(request, 'VTS_Developer_Portal/developer_result.html', {'results': results})
