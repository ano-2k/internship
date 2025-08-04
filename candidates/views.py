from rest_framework import generics, permissions
from .models import CandidateProfile, Internship
from .serializers import CandidateProfileSerializer
from Interview_Questions.permissions import IsCandidate  # Add this import if IsCandidate is defined in permissions.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError





class CandidateProfileCreateView(generics.CreateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsCandidate]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CandidateProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsCandidate]
    def get_object(self):
        return self.request.user.candidate_profile


from .models import InternshipApplication
from .serializers import InternshipApplicationSerializer,CandidateAcceptedApplicationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_internship_applications(request):
    internships = Internship.objects.filter(created_by=request.user)
    applications = InternshipApplication.objects.filter(internship__in=internships).order_by('-applied_at')
    serializer = InternshipApplicationSerializer(applications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_accepted_applications(request):
#     internships = Internship.objects.filter(created_by=request.user)
#     accepted_applications = InternshipApplication.objects.filter(
#         internship__in=internships,
#         status='accepted'
#     ).order_by('-applied_at')

#     serializer = CandidateAcceptedApplicationSerializer(accepted_applications, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_accepted_applications(request):
    internships = Internship.objects.filter(created_by=request.user)

    accepted_applications = InternshipApplication.objects.filter(
        internship__in=internships,
        status='accepted'
    ).order_by('-applied_at')

    serializer = CandidateAcceptedApplicationSerializer(accepted_applications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_application(request, pk):
    try:
        application = InternshipApplication.objects.get(pk=pk, user=request.user)
    except InternshipApplication.DoesNotExist:
        return Response({"error": "Not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InternshipApplicationSerializer(application, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_application(request, pk):
    try:
        application = InternshipApplication.objects.get(pk=pk, user=request.user)
    except InternshipApplication.DoesNotExist:
        return Response({"error": "Not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

    application.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import get_object_or_404

class ApplyInternshipView(generics.CreateAPIView):
    serializer_class = InternshipApplicationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        internship_id = request.data.get("internship")
        internship = get_object_or_404(Internship, id=internship_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, internship=internship)
            return Response({"message": "Application submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
from rest_framework.views import APIView
class AcceptApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            application = InternshipApplication.objects.get(pk=pk)
            application.status = 'accepted'
            application.save()
            return Response({'message': 'Application accepted successfully.'}, status=status.HTTP_200_OK)
        except InternshipApplication.DoesNotExist:
            return Response({'error': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)

class RejectApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            application = InternshipApplication.objects.get(pk=pk)
            application.status = 'rejected'
            application.save()
            return Response({'message': 'Application rejected successfully.'}, status=status.HTTP_200_OK)
        except InternshipApplication.DoesNotExist:
            return Response({'error': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        
 

from candidates.models import FaceToFaceInterview
# from candidates.serializers import FaceToFaceInterviewSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_f2f(request):

    app_id = request.data.get("application_id")
    zoom = request.data.get("zoom")
    date = request.data.get("date")
    time = request.data.get("time")

    try:
        application = InternshipApplication.objects.get(id=app_id, status='accepted')

        # Prevent duplicate interview
        if FaceToFaceInterview.objects.filter(application=application).exists():
            return Response({'error': 'Face to face interview already scheduled for this candidate.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate Zoom URL
        validate = URLValidator()
        try:
            validate(zoom)
        except ValidationError:
            return Response({'error': 'Please enter a valid Zoom URL.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create interview
        FaceToFaceInterview.objects.create(
            application=application,
            name=application.candidate_name,
            internship_role=application.internship_role,
            zoom=zoom,
            date=date,
            time=time 
        )

        return Response({'message': 'Interview scheduled successfully.'}, status=status.HTTP_201_CREATED)

    except InternshipApplication.DoesNotExist:
        return Response({'error': 'Application not found or not accepted.'}, status=status.HTTP_404_NOT_FOUND)







@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_f2f(request, pk):
    try:
        f2f = FaceToFaceInterview.objects.get(pk=pk)
        f2f.delete()
        return Response({'message': 'Interview deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    except FaceToFaceInterview.DoesNotExist:
        return Response({'error': 'Interview record not found.'}, status=status.HTTP_404_NOT_FOUND)


from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_f2f(request, pk):
    try:
        f2f = FaceToFaceInterview.objects.get(pk=pk)

        zoom = request.data.get("zoom")
        date = request.data.get("date")
        time = request.data.get("time")

        # Validate and update Zoom URL
        if zoom is not None:
            validator = URLValidator()
            try:
                validator(zoom)
                f2f.zoom = zoom
            except ValidationError:
                return Response({'error': 'Invalid Zoom URL. It must start with http:// or https://'}, status=status.HTTP_400_BAD_REQUEST)

        # Update date directly (assuming frontend calendar ensures valid format)
        if date is not None:
            f2f.date = date
        if time is not None:
            f2f.time = time if time else None
        f2f.save()
        return Response({'message': 'Interview updated successfully.'}, status=status.HTTP_200_OK)

    except FaceToFaceInterview.DoesNotExist:
        return Response({'error': 'Interview record not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def candidate_application_counts(request):
    user = request.user
    from django.db.models import Count, Q
    
    # Filter all applications by this user (candidate)
    queryset = InternshipApplication.objects.filter(user=user)
    
    counts = queryset.aggregate(
        applied=Count('id'),
        approved=Count('id', filter=Q(status='accepted')),
        rejected=Count('id', filter=Q(status='rejected'))
    )
    
    return Response(counts, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def candidate_scheduled_interviews(request):
    user = request.user

    # Get all applications of this user
    applications = InternshipApplication.objects.filter(user=user)

    # Get all interviews linked to those applications
    interviews = FaceToFaceInterview.objects.filter(application__in=applications)

    interview_data = [
        {
            'id': interview.id,
            'role': interview.internship_role,
            'date': interview.date,
            'time': interview.time,
            'zoom': interview.zoom,
            'company': interview.application.company_name if interview.application else None,
        }
        for interview in interviews
    ]

    return Response({
        'count': interviews.count(),
        'interviews': interview_data
    }, status=status.HTTP_200_OK)
    
    
    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interviewer_dashboard_stats(request):
    user = request.user

    # Internships posted by this interviewer
    internships = Internship.objects.filter(created_by=user)
    total_jobs_posted = internships.count()

    # All applications to their internships
    applications = InternshipApplication.objects.filter(internship__in=internships)
    total_applications = applications.count()
    total_accepted = applications.filter(status='accepted').count()
    total_rejected = applications.filter(status='rejected').count()

    # Scheduled interviews by this interviewer
    interviews = FaceToFaceInterview.objects.filter(application__in=applications)

    interview_data = [
        {
            'id': interview.id,
            'candidate_name': interview.name,
            'internship_role': interview.internship_role,
            'date': interview.date,
            'time': interview.time.strftime('%I:%M %p') if interview.time else None,
            'zoom': interview.zoom,
            'company_name': interview.application.company_name if interview.application else None,
        }
        for interview in interviews
    ]

    return Response({
        'counts': {
            'total_jobs_posted': total_jobs_posted,
            'total_applications_received': total_applications,
            'total_accepted': total_accepted,
            'total_rejected': total_rejected,
        },
        'scheduled_interviews': interview_data,
    }, status=status.HTTP_200_OK)
   
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interview_calendar(request):
    user = request.user
    internships = Internship.objects.filter(created_by=user)
    applications = InternshipApplication.objects.filter(internship__in=internships)
    interviews = FaceToFaceInterview.objects.filter(application__in=applications)

    interview_data = [
        {
            'id': interview.id,
            'candidate_name': interview.name,
            'internship_role': interview.internship_role,
            'date': interview.date.isoformat(),
            'time': interview.time.strftime('%I:%M %p') if interview.time else None,
            'zoom': interview.zoom,
            'company_name': interview.application.company_name if interview.application else None,
        }
        for interview in interviews
    ]

    return Response({
        'scheduled_interviews': interview_data,
    }, status=status.HTTP_200_OK)