from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

from exam.forms import ExamForm, ExamQuestionForm
from exam.models import Exam, ExamQuestion
from .models import Course, User  # use your custom user model
from django.contrib.auth import get_user_model
from .models import Trainer
from .models import Trainee

from .forms import TraineeUserForm, TrainerUserForm
# from .forms import TrainerForm
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
    exams = Exam.objects.all().order_by('-date')  

    search_exam = request.GET.get('e', '') 
    if search_exam:
     exams = exams
     exams = exams.filter(
    Q(course__name__icontains=search_exam) |
    Q(date__icontains=search_exam) |
    Q(title__icontains=search_exam)
     )
     

    
    
    return render(request, 'VTS_Admin_Portal/admin_exam_list.html', {'exams': exams})

def add_exam(request):
    form = ExamForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('exam_list')
    return render(request, 'VTS_Admin_Portal/admin_add_edit_exam.html', {'form': form, 'mode': 'Add'})

def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
   
    questions = ExamQuestion.objects.filter(exam=exam)
    
    
    form = ExamForm(request.POST or None, instance=exam)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('exam_list')
    return render(request, 'VTS_Admin_Portal/admin_add_edit_exam.html', {'form': form, 'mode': 'Edit','questions': questions})

def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()
    return redirect('exam_list')


def add_exam_question_form(request):
    exam_id = request.GET.get('exam_id')

    
    
    if request.method == 'POST':
        form = ExamQuestionForm(request.POST)
        if exam_id:
            form.fields['exam'].initial = exam_id    
            form.fields['exam'].disabled = True
        if form.is_valid():
            form.save()
            return redirect('add_exam_question_form') 
    else:
        form = ExamQuestionForm()
        if exam_id:
            form.fields['exam'].initial = exam_id    
            form.fields['exam'].disabled = True
    

       
        

    return render(request, 'VTS_Admin_Portal/add_question.html', {'form': form, 'exam_id':exam_id})

def edit_exam_question_form(request, question_id):
    question = get_object_or_404(ExamQuestion, id=question_id)
    form = ExamQuestionForm(request.POST or None, instance=question)

    if question.exam:
        form.fields['exam'].initial = question.exam.id
        form.fields['exam'].disabled = True

    if request.method == 'POST' and form.is_valid():
        form.save()
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
    return redirect('exam_list')


def practical_question_list(request):
    questions = PracticalQuestion.objects.all().order_by('-created_at') 
    
    if request.user.role in ['developer', 'designer']:
       trainer = Trainer.objects.get(user=request.user)
       courses = Course.objects.filter(trainer=trainer)
       
      

    # Filter practical questions for courses assigned to this trainer
       questions = PracticalQuestion.objects.filter(course__in=courses).order_by('-id')
      

    

    form = PracticalQuestionForm()

    if request.method == 'POST':
        form = PracticalQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('practical_question_list')  # or reload the same page
    else:
        form = PracticalQuestionForm()
    return render(request, 'VTS_Admin_Portal/practical_question_list.html', {'questions': questions, 'form': form})

def delete_practical_question(request, pk):
    question = get_object_or_404(PracticalQuestion, pk=pk)
    question.delete()
    return redirect('practical_question_list')


from exam.models import PracticalAnswer

def practical_answer_list(request, question_id):
    
    # Get the question
    question = get_object_or_404(PracticalQuestion, id=question_id)

    # Get all answers for that question
    answers = PracticalAnswer.objects.filter(question=question).select_related('trainee__user', 'question').order_by('submitted_at')

    return render(request, 'VTS_Admin_Portal/practical_answer_list.html', {
        'question': question,
        'answers': answers
    })









def admin_logout(request):
    logout(request)
    return redirect('login')





def developer_list_view(request):
    role = request.GET.get('role', 'developer')  # default to 'developer'
    search_trainer = request.GET.get('t', '')    # search term from URL param ?t=

    # Step 1: Filter by role and active status
    developers = Trainer.objects.filter(user__role=role, is_active=True)

    title_map = {
        'developer': 'Developer',
        'designer': 'Designer',
    }
    title = title_map.get(role, 'Developer')

    # Step 2: Filter only the already-role-filtered queryset if search exists
    if search_trainer:
        developers = developers.filter(
            Q(user__full_name__icontains=search_trainer) |
            Q(user__email__icontains=search_trainer) |
            Q(user__mobile__icontains=search_trainer)
        )
        title = 'Filtered Trainers'

    return render(request, 'VTS_Admin_Portal/developer_list.html', {
        'developers': developers,
        'selected_role': role,
        'title': title,
        'search_trainer': search_trainer,
    })

def trainer_form_view(request, trainer_id=None):
    trainer = None
    user = None
    selected_role = request.GET.get('role')
    
    trainers = Trainer.objects.all()
    course = Course.objects.all()
    print('trainers',trainers)

    if trainer_id:
        trainer = get_object_or_404(Trainer, id=trainer_id)
        user = trainer.user

    if request.method == 'POST':
        form = TrainerUserForm(request.POST, request.FILES, initial={'email': user.email} if user else None)
        if form.is_valid():
            if trainer:
                # Edit existing
                user.full_name = form.cleaned_data['full_name']
                user.email = form.cleaned_data['email']
                user.mobile = form.cleaned_data['mobile']
                if form.cleaned_data.get('profile_image'):
                    user.profile_image = form.cleaned_data['profile_image']
                user.role = form.cleaned_data['role']
                user.is_staff = form.cleaned_data.get('is_staff', False)
                user.is_active = form.cleaned_data.get('is_active', True)
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data['password'])
                user.save()

                trainer.gender = form.cleaned_data['gender']
                trainer.dob = form.cleaned_data['dob']
               
                trainer.expertise_area = form.cleaned_data['expertise_area']
                trainer.experience_years = form.cleaned_data['experience_years']
                trainer.technical_languages = form.cleaned_data['technical_languages']
                trainer.address_line1 = form.cleaned_data['address_line1']
                trainer.address_line2 = form.cleaned_data['address_line2']
                trainer.city = form.cleaned_data['city']
                trainer.state = form.cleaned_data['state']
                trainer.postal_code = form.cleaned_data['postal_code']
                trainer.country = form.cleaned_data['country']
                trainer.is_active = form.cleaned_data['is_active']
                trainer.save()
                selected_role =user.role

            else:
                # Create new
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    full_name=form.cleaned_data['full_name'],
                    role=form.cleaned_data['role'],
                    is_staff=form.cleaned_data.get('is_staff', False),
                    is_active=form.cleaned_data.get('is_active', True),
                )
                user.mobile = form.cleaned_data['mobile']
                user.profile_image = form.cleaned_data.get('profile_image')
                user.save()

                Trainer.objects.create(
                    user=user,
                    gender=form.cleaned_data['gender'],
                    dob=form.cleaned_data['dob'],
                    expertise_area=form.cleaned_data['expertise_area'],
                    experience_years=form.cleaned_data['experience_years'],
                    technical_languages=form.cleaned_data['technical_languages'],
                    address_line1=form.cleaned_data['address_line1'],
                    address_line2=form.cleaned_data['address_line2'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    postal_code=form.cleaned_data['postal_code'],
                    country=form.cleaned_data['country'],
                    is_active=form.cleaned_data['is_active'],
                )

            return HttpResponseRedirect(f"{reverse('developer_list')}?role={selected_role}")
    else:
        if trainer:
            form = TrainerUserForm(initial={
                'full_name': user.full_name,
                'email': user.email,
                'mobile': user.mobile,
                'profile_image': user.profile_image,
                'role': user.role,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'gender': trainer.gender,
                'dob': trainer.dob,
                'expertise_area': trainer.expertise_area,
                'experience_years': trainer.experience_years,
                'technical_languages': trainer.technical_languages,
                'address_line1': trainer.address_line1,
                'address_line2': trainer.address_line2,
                'city': trainer.city,
                'state': trainer.state,
                'postal_code': trainer.postal_code,
                'country': trainer.country,
                'is_active': trainer.is_active,
            })
            selected_role =user.role
        else:
            form = TrainerUserForm(initial={'role': selected_role})
           
            

    return render(request, 'VTS_Admin_Portal/trainer_form.html', {
        'form': form,
        'is_edit': bool(trainer),
        'selected_role': selected_role,
        'trainers':trainers,
        'course':course

    })

def trainer_delete_view(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    user = trainer.user  
    role = trainer.user.role
    user.delete()  

    return redirect(f"{reverse('developer_list')}?role={role}") 




def trainee_card_view(request):
    trainees = Trainee.objects.all()
    role = request.GET.get('role', 'developer_trainee') 

     # New filters from form
    selected_class_mode = request.GET.get('class_mode')
    selected_course_id = request.GET.get('course')
    selected_trainer_id = request.GET.get('trainer')

    # Base queryset

    # Apply filters
    if selected_class_mode:
        trainees = trainees.filter(class_mode=selected_class_mode)
    if selected_course_id:
        trainees = trainees.filter(assigned_course_id=selected_course_id)
    if selected_trainer_id:
        trainees = trainees.filter(assigned_trainer_id=selected_trainer_id)
    return render(request, 'VTS_Admin_Portal/trainee_card_list.html', {'trainees': trainees,'selected_class_mode': selected_class_mode,
        'selected_course_id': selected_course_id,
        'selected_trainer_id': selected_trainer_id,'selected_role':role,})

from django.db.models import Q

def trainee_list_view(request):
    role = request.GET.get('role', 'developer_trainee') 
    search_query = request.GET.get('q', '') 
    trainees = Trainee.objects.filter(user__role=role, is_active=True)
    trainers = Trainer.objects.all()
    course = Course.objects.all()
    

    title_map = {
        
        'developer_trainee': 'Developer_Trainee',
        'designer_trainee': 'Designer_Trainee',
    }
    title = title_map.get(role, 'Developer_Trainee')


    if search_query:
      
      title = 'All Trainees'
     

      trainees = trainees.filter(
        Q(user__full_name__icontains=search_query) |
        Q(user__email__icontains=search_query) |
        Q(user__mobile__icontains=search_query)
     )
      
     

       

    


    return render(request, 'VTS_Admin_Portal/trainee_list.html', {'trainees': trainees, 'title': title,  'search_query': search_query, 'selected_role':role,'trainers':trainers,
        'course':course})




def trainee_form_view(request, trainee_id=None):
    trainee = None
    user = None
    selected_role = request.GET.get('role')

    if trainee_id:
        trainee = get_object_or_404(Trainee, id=trainee_id)
        user = trainee.user
        selected_role = trainee.user.role

    if request.method == 'POST':
        form = TraineeUserForm(request.POST, request.FILES, initial={'email': user.email} if user else None)
        if form.is_valid():
            assigned_course = form.cleaned_data['assigned_course']
            assigned_trainer = assigned_course.trainer  # Auto-get trainer
            start_date = assigned_course.start_date

            if trainee:
                # Edit
                user.full_name = form.cleaned_data['full_name']
                user.email = form.cleaned_data['email']
                user.mobile = form.cleaned_data['mobile']
                if form.cleaned_data.get('profile_image'):
                    user.profile_image = form.cleaned_data['profile_image']
                user.role = form.cleaned_data['role']
                user.is_staff = form.cleaned_data.get('is_staff', False)
                user.is_active = form.cleaned_data.get('is_active', True)
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data['password'])
                user.save()

                trainee.gender = form.cleaned_data['gender']
                trainee.dob = form.cleaned_data['dob']
                trainee.class_mode = form.cleaned_data['class_mode']
                trainee.assigned_course = assigned_course
                trainee.assigned_trainer = assigned_trainer  # auto-filled
                trainee.start_date = start_date
                trainee.address_line1 = form.cleaned_data['address_line1']
                trainee.address_line2 = form.cleaned_data['address_line2']
                trainee.city = form.cleaned_data['city']
                trainee.state = form.cleaned_data['state']
                trainee.postal_code = form.cleaned_data['postal_code']
                trainee.country = form.cleaned_data['country']
                # trainee.is_active = form.cleaned_data['is_active']
                trainee.save()

            else:
                # Create
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    full_name=form.cleaned_data['full_name'],
                    role=form.cleaned_data['role'],
                    # is_staff=form.cleaned_data.get('is_staff', False),
                    # is_active=form.cleaned_data.get('is_active', True),
                )
                user.mobile = form.cleaned_data['mobile']
                user.profile_image = form.cleaned_data.get('profile_image')
                user.save()

                Trainee.objects.create(
                    user=user,
                    gender=form.cleaned_data['gender'],
                    dob=form.cleaned_data['dob'],
                    class_mode=form.cleaned_data['class_mode'],
                    assigned_course=assigned_course,
                    assigned_trainer=assigned_trainer,  # auto-filled
                    start_date=start_date,
                    address_line1=form.cleaned_data['address_line1'],
                    address_line2=form.cleaned_data['address_line2'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    postal_code=form.cleaned_data['postal_code'],
                    country=form.cleaned_data['country'],
                    # is_active=form.cleaned_data['is_active'],
                )

            return redirect(f"{reverse('trainee_list')}?role={user.role}")
    else:
        if trainee:
            form = TraineeUserForm(initial={
                'full_name': user.full_name,
                'email': user.email,
                'mobile': user.mobile,
                'profile_image': user.profile_image,
                'role': user.role,
                # 'is_staff': user.is_staff,
                # 'is_active': user.is_active,

                'gender': trainee.gender,
                'dob': trainee.dob.strftime('%Y/%m/%d') if trainee.dob else '',
                'class_mode': trainee.class_mode,
                'assigned_course': trainee.assigned_course,
                # 'assigned_trainer': trainee.assigned_trainer,  # Not needed in form
                # 'start_date': trainee.start_date.strftime('%Y/%m/%d') if trainee.start_date else '',
                'address_line1': trainee.address_line1,
                'address_line2': trainee.address_line2,
                'city': trainee.city,
                'state': trainee.state,
                'postal_code': trainee.postal_code,
                'country': trainee.country,
                'is_active': trainee.is_active,
            })
        else:
            form = TraineeUserForm(initial={'role': selected_role})

    return render(request, 'VTS_Admin_Portal/trainee_form.html', {
        'form': form,
        'is_edit': bool(trainee),
        'trainee': trainee,
        'selected_role': selected_role
    })


def trainee_delete_view(request, trainee_id):
    trainee = get_object_or_404(Trainee, id=trainee_id)
    selected_role = request.GET.get('role')
   
    user = trainee.user
    user.delete()
    return redirect(f"{reverse('trainee_list')}?role={selected_role}")

from .forms import CourseForm

def course_list(request):
    courses = Course.objects.all()
    search_course = request.GET.get('c', '') 
    if search_course:
     courses = courses
     courses = courses.filter(
    Q(name__icontains=search_course) 
   
     )
        
    return render(request, 'VTS_Admin_Portal/course_list.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            print("Start Date:", start_date)
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'VTS_Admin_Portal/course_form.html', {'form': form, 'title': 'Add Course'})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'VTS_Admin_Portal/course_form.html', {'form': form, 'title': 'Edit Course','is_edit': bool(course)})

def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('course_list') 