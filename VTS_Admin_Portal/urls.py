from django.urls import path
from . import views

urlpatterns = [
      
       path('', views.login_view, name='login'),

   path('login/', views.login_view, name='login'),

   path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

   
    path('dashboard/designer/', views.designer_dashboard, name='designer_dashboard'),
    path('developer_dashboard/', views.developer_dashboard, name='developer_dashboard'),
    path('dashboard/designer-trainee/', views.designer_trainee_dashboard, name='designer_trainee_dashboard'),
    path('dashboard/developer-trainee/', views.developer_trainee_dashboard, name='developer_trainee_dashboard'),

    path('logout/', views.admin_logout, name='admin_logout'),
      path('developer_list/', views.developer_list_view, name='developer_list'),
     path('trainers/add/', views.trainer_form_view, name='add_trainer'),
    path('trainers/<int:trainer_id>/edit/', views.trainer_form_view, name='edit_trainer'),
    path('trainers/<int:trainer_id>/delete/', views.trainer_delete_view, name='delete_trainer'),


path('trainees/trainee_card_view', views.trainee_card_view, name='trainee_card_view'),
     path('trainees/', views.trainee_list_view, name='trainee_list'),
    path('trainees/add/', views.trainee_form_view, name='add_trainee'),
    path('trainees/<int:trainee_id>/edit/', views.trainee_form_view, name='edit_trainee'),
    path('trainees/<int:trainee_id>/delete/', views.trainee_delete_view, name='delete_trainee'),

     path('exams/exam_list/', views.exam_list, name='exam_list'),
     path('exams/add/', views.add_exam, name='add_exam'),
    path('exams/<int:exam_id>/edit/', views.edit_exam, name='edit_exam'),
    path('exams/<int:exam_id>/delete/', views.delete_exam, name='delete_exam'),
    path('exams/add_exam_question_form/', views.add_exam_question_form, name='add_exam_question_form'),

    
path('exams/edit_exam_question_form/<int:question_id>/', views.edit_exam_question_form, name='edit_exam_question_form'),
    
    path('exams/add-question/', views.add_exam_question, name='add_exam_question'),
     path('questions/<int:question_id>/delete/', views.delete_exam_question, name='delete_question'),

      path('practicalquestions/', views.practical_question_list, name='practical_question_list'),
    path('practicalquestions/delete/<int:pk>/', views.delete_practical_question, name='delete_practical_question'),
    path('answers/', views.practical_answer_list, name='practical_answer_list'),


]
