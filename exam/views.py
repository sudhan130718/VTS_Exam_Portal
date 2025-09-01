from django.shortcuts import render, redirect, get_object_or_404

from VTS_Admin_Portal.models import Trainee, Trainer
from .models import Exam, ExamQuestion, TraineeExam, TraineeAnswer
from .forms import ExamForm, ExamQuestionForm
from django.utils import timezone
from .forms import ExamForm  # We'll create this below
from django.contrib import messages

def create_exam(request):
    form = ExamForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('create_exam')
    return render(request, 'exam/create_exam.html', {'form': form})

def add_exam_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    print('exam',exam)
    form = ExamQuestionForm(request.POST or None, initial={'exam': exam})
    if form.is_valid():
        form.save()
        return redirect('add_exam_question', exam_id=exam_id)
    return render(request, 'exam/add_question.html', {'form': form, 'exam': exam})




def available_exams(request):
    trainee = request.user.trainee_profile
    trainee_exams = TraineeExam.objects.filter(trainee=trainee, attended=False)
    return render(request, 'exam/available_exams.html', {'trainee_exams': trainee_exams})

def start_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    print('user', request.user.trainee_profile)
    trainee = request.user.trainee_profile
    trainee_exam, created = TraineeExam.objects.get_or_create(trainee=trainee, exam=exam)
    questions = exam.questions.all()
    return render(request, 'exam/start_exam.html', {'exam': exam, 'questions': questions, 'trainee_exam': trainee_exam})

def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    trainee = request.user.trainee_profile
    trainee_exam = get_object_or_404(TraineeExam, trainee=trainee, exam=exam)
    score = 0

    for question in exam.questions.all():
        selected = request.POST.get(str(question.id))
        TraineeAnswer.objects.create(
            trainee_exam=trainee_exam,
            question=question,
            selected_option=selected
        )
        if selected == question.correct_option:
            score += 1

    trainee_exam.score = score
    trainee_exam.attended = True
    trainee_exam.submitted_at = timezone.now()
    trainee_exam.save()

    return render(request, 'exam/result.html', {'score': score, 'total': exam.questions.count()})


# from django.db.models import Q

# def exam_result_list(request):
#     results = TraineeExam.objects.select_related('trainee__user', 'exam').all().order_by('-submitted_at')
#     exam_id = request.GET.get('exam_id')
#     print("exam_id",exam_id)
#     if exam_id:
#         results = results.filter(exam__id=exam_id)

#     search_result = request.GET.get('r', '')
#     if search_result:
#      results = results
     

#      results = results.filter(
#         Q(trainee__user__full_name__icontains=search_result) |
#         Q(submitted_at__icontains=search_result) |
#         Q(exam__title__icontains=search_result)
         
 
       
#     )
#     return render(request, 'exam/exam_result_list.html', {'results': results})


from django.db.models import Q, Max, Sum
from .models import TraineeExam

def exam_result_list(request):
    exam_id = request.GET.get('exam_id')
    total_trainees =0
    total_marks =0
    present_count = 0
    absent_count =0
   
    search_result = request.GET.get('r', '')



    # results = TraineeExam.objects.select_related('trainee__user', 'exam')
    trainer = Trainer.objects.get(user=request.user) 
    results = TraineeExam.objects.select_related('trainee__user', 'exam').filter(
    trainee__assigned_trainer=trainer
)
      
    print("Result_New", results)


    

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
    print("Result", results)

    # ---- Card Stats ----
    # total_trainees = results.values('trainee_id').distinct().count()
    
    # total_marks = results.aggregate(total=Sum('exam__total_marks'))['total'] or 0
    
    
    # absent_count = results.filter(score=None).count()
    

    return render(request, 'exam/exam_result_list.html', {
        'results': results,
        'total_trainees': total_trainees,
        'total_marks': total_marks,
        'present_count': present_count,
        'absent_count': absent_count,
    })






