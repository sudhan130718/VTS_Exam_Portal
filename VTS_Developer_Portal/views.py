from django.shortcuts import render,get_object_or_404

from VTS_Admin_Portal.models import Trainee, Trainer
from exam.models import Exam, TraineeExam

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

 
    exams = Exam.objects.all().order_by('-date')  # Optional: newest first
    
    return render(request, 'VTS_Developer_Portal/developer_exam.html', {'exams': exams})

def developer_result(request):
    results = TraineeExam.objects.select_related('trainee__user', 'exam').all().order_by('-submitted_at')
    return render(request, 'VTS_Developer_Portal/developer_result.html', {'results': results})
