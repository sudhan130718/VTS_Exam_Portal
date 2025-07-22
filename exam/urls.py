from django.urls import path
from . import views

urlpatterns = [
    path('exams/add/', views.create_exam, name='create_exam'),
    path('exams/<int:exam_id>/add-question/', views.add_exam_question, name='add_exam_question'),
   
    path('exams/available/', views.available_exams, name='available_exams'),
    path('exams/<int:exam_id>/start/', views.start_exam, name='start_exam'),
    path('exams/<int:exam_id>/submit/', views.submit_exam, name='submit_exam'),

    path('exam/results/', views.exam_result_list, name='exam_result_list'),
    # path('exam/results/<int:exam_id>/', views.exam_result_list, name='exam_result_list'),


]
