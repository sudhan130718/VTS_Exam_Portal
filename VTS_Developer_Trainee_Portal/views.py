from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from VTS_Admin_Portal.models import Trainee
from exam.forms import PracticalAnswerForm
from exam.models import Exam, PracticalQuestion, TraineeAnswer, TraineeExam
from xhtml2pdf import pisa
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
import io

# Create your views here.

def developer_trainee_dashboard(request):
       trainee = get_object_or_404(Trainee, user=request.user)
       questions = PracticalQuestion.objects.all().order_by('-created_at')
       
     
       return render(request, 'VTS_Developer_Trainee_Portal/developer_trainee_dashboard.html', {'trainee': trainee ,'questions': questions})
               
          
from django.db.models import Count

def developer_trainee_exam(request):
        trainee = get_object_or_404(Trainee, user=request.user)
        
 
     # Get exams for the trainee's course
        exams = Exam.objects.filter(course=trainee.assigned_course ).order_by('date', 'start_time')
        # exams = Exam.objects.all()
        # questions = PracticalQuestion.objects.all().order_by('-created_at')
        questions = PracticalQuestion.objects.filter(course=trainee.assigned_course ).order_by('-created_at')


        trainee_exam_map = {}
        for exam in exams:
         trainee_exam = TraineeExam.objects.filter(trainee=trainee, exam=exam).first()
         trainee_exam_map[exam.id] = trainee_exam


        if request.method == 'POST':
         question_id = request.POST.get('question_id')
         question = get_object_or_404(PracticalQuestion, id=question_id)
         form = PracticalAnswerForm(request.POST, request.FILES)
         if form.is_valid():
            answer = form.save(commit=False)
            answer.trainee = trainee
            answer.question = question
            answer.save()
            return redirect('developer_trainee_dashboard')
        else:
         form = PracticalAnswerForm()



        return render(request, 'VTS_Developer_Trainee_Portal/developer_trainee_exam.html', {
        'trainee': trainee,
        'exams': exams,
        'questions': questions,
        'form': form,
        'trainee_exam_map': trainee_exam_map
        })

def developer_trainee_start_exam(request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)
        trainee = get_object_or_404(Trainee, user=request.user)
        trainee_exam, created = TraineeExam.objects.get_or_create(trainee=trainee, exam=exam)
        questions = exam.questions.all()
        exam_duration =exam.duration_minutes
        print('exam_duration',exam_duration)
       

        return render(request, 'VTS_Developer_Trainee_Portal/developer_trainee_start_exam.html', {
        'trainee': trainee,'questions': questions, 'trainee_exam': trainee_exam,'exam':exam, 'exam_duration': exam_duration
        
        })

import base64
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

def developer_trainee_submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    trainee = request.user.trainee_profile
    trainee_exam = get_object_or_404(TraineeExam, trainee=trainee, exam=exam)

    if request.method == "POST":
        import json
        image_data = request.POST.get("image")
        print("Raw request.body:", image_data)

        # data = json.loads(request.body)
        # image_data = data.get("image")

       

        
        if image_data:
            format, imgstr = image_data.split(';base64,') 
            ext = format.split('/')[-1]  
            file_data = ContentFile(base64.b64decode(imgstr), name=f"snapshot.{ext}")
            
            TraineeExam.objects.create(image=file_data)

    

    if trainee_exam.attended:
        messages.warning(request, "You have already submitted this exam.")
        return redirect('developer_trainee_all_results')
    
    
    score = 0

    for question in exam.questions.all():
        selected = request.POST.get(f'q{question.id}')

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

    return render(request, 'VTS_Developer_Trainee_Portal/developer_trainee_exam_result.html', {'exam':exam, 'score': score, 'total': exam.questions.count()})

def developer_trainee_all_results(request):
   results = TraineeExam.objects.select_related('trainee', 'exam') \
    .filter(trainee__user=request.user) \
    .order_by('-submitted_at')   
   return render(request, 'VTS_Developer_Trainee_Portal/developer_trainee_all_results.html', {'results': results})

def download_exam_result(request, result_id):
    trainee = request.user.trainee_profile  # or however you're linking
    result = get_object_or_404(TraineeExam, id=result_id, trainee=trainee)

    template = get_template('exam/result_pdf_template.html')
    html = template.render({
        'exam': result.exam.title,
        'trainee_exam': result.trainee.user.full_name,
        'score': result.score,
        'total': result.exam.total_marks,
        'trainer':result.trainee.assigned_trainer,
        'course':result.trainee.assigned_course,
          'date':result.submitted_at 

    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="result_{result.exam.title}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had an error while generating PDF')
    return response