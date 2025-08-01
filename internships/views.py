from rest_framework import generics, permissions
from .models import Internship
from .serializers import InternshipSerializer
from .permissions import IsEmployee,IsCandidate

# Create - only employee
class InternshipCreateView(generics.CreateAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [IsEmployee]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# List all
class InternshipListView(generics.ListAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [IsEmployee]  # Restrict to employees

    def get_queryset(self):
        # Filter internships by the authenticated user
        return Internship.objects.filter(created_by=self.request.user).order_by('-created_at')

# Retrieve by ID
class InternshipDetailView(generics.RetrieveAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAuthenticated]

# Update - only creator employee
class InternshipUpdateView(generics.UpdateAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [IsEmployee]
    queryset = Internship.objects.all()

    def get_queryset(self):
        return Internship.objects.filter(created_by=self.request.user)

# Delete - only creator employee
class InternshipDeleteView(generics.DestroyAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [IsEmployee]
    queryset = Internship.objects.all()

    def get_queryset(self):
        return Internship.objects.filter(created_by=self.request.user)

class AllInternshipsListView(generics.ListAPIView):
    serializer_class = InternshipSerializer
    permission_classes = [IsCandidate]  # Restrict to candidates
    queryset = Internship.objects.all().order_by('-created_at')
    
    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FaceToFaceInterview
from .serializers import FaceToFaceInterviewSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_face_to_face_interview(request):
    if request.user.role != 'employee':
        return Response({"detail": "Unauthorized"}, status=403)

    interviews = FaceToFaceInterview.objects.filter(user=request.user)
    serializer = FaceToFaceInterviewSerializer(interviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def face_to_face_interview_update(request, pk):
    interview = get_object_or_404(FaceToFaceInterview, pk=pk)

    if interview.user != request.user or request.user.role != 'employee':
        return Response({"detail": "Unauthorized"}, status=403)

    serializer = FaceToFaceInterviewSerializer(interview, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def face_to_face_interview_delete(request, pk):
    interview = get_object_or_404(FaceToFaceInterview, pk=pk)

    if interview.user != request.user or request.user.role != 'employee':
        return Response({"detail": "Unauthorized"}, status=403)

    interview.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)