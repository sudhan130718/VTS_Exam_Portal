from django.shortcuts import render,get_object_or_404

from VTS_Admin_Portal.models import Course, Trainee, Trainer
from exam.models import Exam, TraineeExam
from django.db.models import Q
from django.db.models import  Max, Sum
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
    # trainer = Trainer.objects.get(user=request.user) 
    # courses = Course.objects.filter(trainer=trainer)

    # exams = Exam.objects.filter(course__in=courses).order_by('-id')
    exams = Exam.objects.all()
    search_exam = request.GET.get('e', '') 
    if search_exam:
     exams = exams
     exams = exams.filter(
    Q(course__name__icontains=search_exam) |
    Q(course__trainer__user__full_name__icontains=search_exam) |
    Q(date__icontains=search_exam) |
    Q(title__icontains=search_exam)
     )


    return render(request, 'VTS_Developer_Portal/developer_exam.html', {'exams': exams})

def developer_result(request):
    exam_id = request.GET.get('exam_id')

    total_trainees =0
    total_marks =0
    present_count = 0
    absent_count =0
   
    search_result = request.GET.get('r', '')




    # results = TraineeExam.objects.select_related('trainee__user', 'exam')
    # trainer = Trainer.objects.get(user=request.user) 
    results = TraineeExam.objects.all()

      


    

    # Filter by exam ID if provided
    if exam_id:
        results = results.filter(exam__id=exam_id)
        exam = Exam.objects.get(id=exam_id)  # now it's a model instance
        
        trainees = Trainee.objects.filter(assigned_course=exam.course)
        trainees_count = trainees.count()  
        total_trainees =trainees_count
        total_marks =exam.total_marks
        present_count = results.exclude(score=None).count()
        absent_count =total_trainees-present_count

        

    # Filter by search query if provided
    if search_result:

        results = results.filter(
            Q(trainee__user__full_name__icontains=search_result) |
            Q(submitted_at__icontains=search_result) |
            Q(exam__title__icontains=search_result)
        )

    # If no filter/search, get only latest submitted result per trainee
    if not (exam_id or search_result):
        latest_submissions = (
            TraineeExam.objects.values('trainee_id')
            .annotate(latest_date=Max('submitted_at'))
        )

        latest_dates = [entry['latest_date'] for entry in latest_submissions]
        results = results.filter(submitted_at__in=latest_dates)

    results = results.order_by('-submitted_at')

   
    

   



    # role = request.GET.get('role')

    # results = TraineeExam.objects.all()

    # if role:
    #         results = TraineeExam.objects.filter(exam__title=role).order_by('-submitted_at') 

     
        




    return render(request, 'VTS_Developer_Portal/developer_result.html', {'results': results,
        'total_trainees': total_trainees,
        'total_marks': total_marks,
        'present_count': present_count,
        'absent_count': absent_count,})
