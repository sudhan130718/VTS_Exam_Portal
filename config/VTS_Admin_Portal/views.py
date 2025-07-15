from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from exam.forms import ExamForm, ExamQuestionForm
from exam.models import Exam, ExamQuestion
from .models import User  # use your custom user model
from django.contrib.auth import get_user_model
from .models import Trainer


from .forms import TrainerForm
from .forms import PracticalQuestionForm
from exam.models import PracticalQuestion




User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # 'username' is input name, but we treat as email
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # ✅ Role-based redirects
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'designer':
                return redirect('developer_dashboard')
            elif user.role == 'developer':
                return redirect('developer_dashboard')
            elif user.role == 'designer_trainee':
                return redirect('developer_trainee_dashboard')
            elif user.role == 'developer_trainee':
                return redirect('developer_trainee_dashboard')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'VTS_Admin_Portal/login.html')


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def admin_dashboard(request):
    # return HttpResponse("Welcome Admin")
    form = PracticalQuestionForm()

    if request.method == 'POST':
        form = PracticalQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # or reload the same page
    else:
        form = PracticalQuestionForm()


    return render(request, 'VTS_Admin_Portal/admin_dashboard.html', {'form': form})

@login_required
def designer_dashboard(request):
    return HttpResponse("Welcome Designer")

@login_required
def developer_dashboard(request):
    # return HttpResponse("Welcome Developer")
    return render(request, 'VTS_Developer_Portal/developer_dashboard.html')


@login_required
def designer_trainee_dashboard(request):
    return HttpResponse("Welcome Designer Trainee")

@login_required
def developer_trainee_dashboard(request):
    
    return render(request, 'VTS_Developer_Trainee_Portal/developer_trainee_dashboard.html')



def exam_list(request):
    exams = Exam.objects.all().order_by('-date')  # Optional: newest first
    
    return render(request, 'VTS_Admin_Portal/admin_exam_list.html', {'exams': exams})

def add_exam(request):
    form = ExamForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Exam added successfully.")
        return redirect('exam_list')
    return render(request, 'VTS_Admin_Portal/admin_add_edit_exam.html', {'form': form, 'mode': 'Add'})

def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
   
    questions = ExamQuestion.objects.filter(exam=exam)
    
    
    form = ExamForm(request.POST or None, instance=exam)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Exam updated successfully.")
        return redirect('exam_list')
    return render(request, 'VTS_Admin_Portal/admin_add_edit_exam.html', {'form': form, 'mode': 'Edit','questions': questions})

def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()
    messages.success(request, "Exam deleted successfully.")
    return redirect('exam_list')

def add_exam_question_form(request):
  
    form = ExamQuestionForm()

    exam_id = request.GET.get('exam_id')
    if exam_id:
        form.fields['exam'].initial = exam_id    
        form.fields['exam'].disabled = True

    return render(request, 'VTS_Admin_Portal/add_question.html', {'form': form})

def edit_exam_question_form(request, question_id):
    question = get_object_or_404(ExamQuestion, id=question_id)
    form = ExamQuestionForm(request.POST or None, instance=question)

    if question.exam:
        form.fields['exam'].initial = question.exam.id
        form.fields['exam'].disabled = True

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Question updated successfully.")
        return redirect('exam_list')

    return render(request, 'VTS_Admin_Portal/add_question.html', {
        'form': form,
        'question': question,
        'mode': 'Edit'
    })




def add_exam_question(request):
    if request.method == 'POST':
        form = ExamQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')  # Change to your desired redirect
    else:
        form = ExamQuestionForm()

  
    return render(request, 'VTS_Admin_Portal/add_question.html', {'form': form})

def delete_exam_question(request, question_id):
    question = get_object_or_404(ExamQuestion, id=question_id)
    exam_id = question.exam.id
    question.delete()
    messages.success(request, "Question deleted successfully.")
    return redirect('exam_list')


def practical_question_list(request):
    questions = PracticalQuestion.objects.all().order_by('-created_at') 

    form = PracticalQuestionForm()

    if request.method == 'POST':
        form = PracticalQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # or reload the same page
    else:
        form = PracticalQuestionForm()
    return render(request, 'VTS_Admin_Portal/practical_question_list.html', {'questions': questions, 'form': form})

def delete_practical_question(request, pk):
    question = get_object_or_404(PracticalQuestion, pk=pk)
    question.delete()
    messages.success(request, "Question deleted successfully.")
    return redirect('practical_question_list')


from exam.models import PracticalAnswer

def practical_answer_list(request):
    answers = PracticalAnswer.objects.select_related('trainee__user', 'question__course').order_by('submitted_at')
    return render(request, 'VTS_Admin_Portal/practical_answer_list.html', {'answers': answers})








def admin_logout(request):
    logout(request)
    return redirect('login')




def developer_list_view(request):
    role = request.GET.get('role', 'developer')  
    developers = Trainer.objects.filter(user__role=role, is_active=True)

    title_map = {
        'developer': 'Developer',
        'designer': 'Designer',
       
    }
    title = title_map.get(role, 'Developer')
    return render(request, 'VTS_Admin_Portal/developer_list.html', {
        'developers': developers,
        'selected_role': role,
         'title': title
    })


def trainer_form_view(request, trainer_id=None):
    instance = None
    if trainer_id:
        instance = get_object_or_404(Trainer, id=trainer_id)

    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('developer_list')  # or your trainer list page
    else:
        form = TrainerForm(instance=instance)

    return render(request, 'VTS_Admin_Portal/trainer_form.html', {
        'form': form,
        'is_edit': bool(instance),
    })

def trainer_delete_view(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    trainer.delete()
    messages.success(request, "Trainer deleted successfully.")
    return redirect('developer_list')  # Or wherever you want to redirect after delete

from .models import Trainee
from .forms import TraineeForm

def trainee_card_view(request):
    trainees = Trainee.objects.all()
    return render(request, 'VTS_Admin_Portal/trainee_card_list.html', {'trainees': trainees})

from django.db.models import Q
def trainee_list_view(request):
    role = request.GET.get('role', 'developer_trainee') 
    search_query = request.GET.get('q', '') 
    trainees = Trainee.objects.filter(user__role=role, is_active=True)
    print("search_query", search_query)
    if search_query:
     trainees = Trainee.objects.all()

     trainees = trainees.filter(
        Q(user__full_name__icontains=search_query) |
        Q(user__email__icontains=search_query) |
        Q(user__mobile__icontains=search_query)
    )

       

    title_map = {
        
        'developer_trainee': 'Developer Trainee',
        'designer_trainee': 'Designer Trainee',
    }
    title = title_map.get(role, 'Developer Trainee')


    return render(request, 'VTS_Admin_Portal/trainee_list.html', {'trainees': trainees, 'title': title,  'search_query': search_query,'selected_role': role,})

def trainee_form_view(request, trainee_id=None):
    if trainee_id:
        trainee = get_object_or_404(Trainee, id=trainee_id)
    else:
        trainee = None

    form = TraineeForm(request.POST or None, request.FILES or None, instance=trainee)
    if form.is_valid():
        form.save()
        return redirect('trainee_list')

    return render(request, 'VTS_Admin_Portal/trainee_form.html', {'form': form, 'trainee': trainee})

def trainee_delete_view(request, trainee_id):
    trainee = get_object_or_404(Trainee, id=trainee_id)
    trainee.delete()
    return redirect('trainee_list')