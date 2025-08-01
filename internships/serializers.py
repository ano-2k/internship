from rest_framework import serializers
from .models import Internship
from .models import FaceToFaceInterview

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']




class FaceToFaceInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceToFaceInterview
        fields = ['id', 'name', 'internship_role', 'date', 'zoom']