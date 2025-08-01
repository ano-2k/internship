from django.urls import path
from .views import CandidateProfileCreateView, CandidateProfileDetailView,ApplyInternshipView
from . import views


urlpatterns = [
    path('profile/create/', CandidateProfileCreateView.as_view(), name='candidate_profile_create'),
    path('profile/', CandidateProfileDetailView.as_view(), name='candidate_profile_detail_update'),
    path('applications/', views.list_internship_applications, name='list-internship-applications'),
    path('applications/<int:pk>/edit/', views.edit_application, name='edit-application'),
    path('applications/<int:pk>/delete/', views.delete_application, name='delete-application'),
    path('apply-internship/', ApplyInternshipView.as_view(), name='apply_internship'),
    
    # path('candidate-applications/', views.candidate_applications, name='candidate-applications'),
    # path('interviewer-applications/', views.interviewer_applications, name='interviewer-applications'),

]

