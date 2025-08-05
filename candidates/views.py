from rest_framework import generics
from internships.models import  Internship
from candidates.serializers import CandidateProfileSerializer
from Interview_Questions.permissions import IsCandidate  # Add this import if IsCandidate is defined in permissions.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated






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
from interviewer.models import FaceToFaceInterview
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
    
    
    