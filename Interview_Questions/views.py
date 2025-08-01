from rest_framework import generics, permissions
from .models import Quiz
from .serializers import QuizSerializer
from .permissions import IsEmployee

# Create Quiz (already provided)
class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsEmployee]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Get All Quizzes
class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

# Get Quiz by ID
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

# Update/Edit Quiz (only employee who created can edit)
class QuizUpdateView(generics.UpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        return Quiz.objects.filter(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):

        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

# Delete Quiz (only employee who created can delete)
class QuizDeleteView(generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        return Quiz.objects.filter(created_by=self.request.user)
    

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from .models import Quiz, Question, Option  # Adjust import based on your models

class ExportQuizExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get module filter from query params
        module = request.query_params.get('module', None)

        # Create the workbook and worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Interview Questions"

        # Write header
        headers = ["Quiz Title", "Question Text", "Option", "Is Correct"]
        ws.append(headers)

        # Gather and write data
        quizzes = Quiz.objects.prefetch_related('questions__options').all()
        if module:
            quizzes = quizzes.filter(title__icontains=module)

        if not quizzes.exists():
            return Response(
                {"detail": "No quizzes found for the specified module."},
                status=status.HTTP_404_NOT_FOUND
            )

        for quiz in quizzes:
            for question in quiz.questions.all():
                for option in question.options.all():
                    ws.append([
                        quiz.title,
                        question.text,
                        option.text,
                        "Yes" if option.is_correct else "No"
                    ])

        # Set column widths
        for col_num, _ in enumerate(headers, 1):
            ws.column_dimensions[get_column_letter(col_num)].width = 30

        # Prepare response
        filename = f"interview_questions_{module or 'all'}.xlsx"
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Save workbook to response
        wb.save(response)
        return response
