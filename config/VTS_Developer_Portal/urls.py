from django.urls import path
from . import views

urlpatterns = [
    path('trainer/developer_dashboard/', views.developer_dashboard, name='developer_dashboard'),
     path('developer_trainee_card_view/', views.developer_trainee_card_view, name='developer_trainee_card_view'),
     path('developer_exam/', views.developer_exam, name='developer_exam'),
      path('developer_result/', views.developer_result, name='developer_result'),

    # path('trainee/developer_trainee_exam/', views.developer_trainee_exam, name='developer_trainee_exam'),
    # path('trainee/developer_trainee_start_exam/<int:exam_id>/', views.developer_trainee_start_exam, name='developer_trainee_start_exam'),
    # path('trainee/submit_exam/<int:exam_id>/', views.developer_trainee_submit_exam, name='developer_trainee_submit_exam'),
    # path('trainee/developer_trainee_all_results/', views.developer_trainee_all_results, name='developer_trainee_all_results'),
    # path('trainee/result/download/<int:exam_id>/', views.download_exam_result, name='download_exam_result'),

]