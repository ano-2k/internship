from django.urls import path
from .views import CandidateProfileCreateView, CandidateProfileDetailView,ApplyInternshipView,AcceptApplicationView, RejectApplicationView
from . import views


urlpatterns = [
    path('profile/create/', CandidateProfileCreateView.as_view(), name='candidate_profile_create'),
    path('profile/', CandidateProfileDetailView.as_view(), name='candidate_profile_detail_update'),
    path('applications/', views.list_internship_applications, name='list-internship-applications'),
    path('applications/<int:pk>/edit/', views.edit_application, name='edit-application'),
    path('applications/<int:pk>/delete/', views.delete_application, name='delete-application'),
    path('apply-internship/', ApplyInternshipView.as_view(), name='apply_internship'),
    
    path('applications/<int:pk>/accept/', AcceptApplicationView.as_view(), name='accept-application'),
    path('applications/<int:pk>/reject/', RejectApplicationView.as_view(), name='reject-application'),
    path('accepted-applications/', views.list_accepted_applications, name='accepted-applications'),
    path('interview/create/', views.create_f2f, name='create-f2f'),
    path('interview/update/<int:pk>/', views.update_f2f, name='update-f2f'),
    path('interview/delete/<int:pk>/', views.delete_f2f, name='delete-f2f'),
    # path('candidate-applications/', views.candidate_applications, name='candidate-applications'),
    # path('interviewer-applications/', views.interviewer_applications, name='interviewer-applications'),
   path('application-counts/', views.candidate_application_counts, name='candidate-application-counts'),
   path('scheduled-interviews/', views.candidate_scheduled_interviews, name='candidate-scheduled-interviews'),
   path('interviewer-dashboard/', views.interviewer_dashboard_stats, name='interviewer-dashboard'),
   path('interviewer/interview_calendar/', views.interview_calendar, name='interview_calendar'),
]

