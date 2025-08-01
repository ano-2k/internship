from rest_framework import serializers
from .models import CandidateProfile
from .models import InternshipApplication

class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = '__all__'
        read_only_fields = ['user']




class InternshipApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='user.username', read_only=True)
    internship_role = serializers.CharField(source='internship.internship_role', read_only=True)
    company_name = serializers.CharField(source='internship.company_name', read_only=True)
    interviewer_name = serializers.CharField(source='internship.created_by.username', read_only=True)
    resume = serializers.FileField()  # if not already included

    class Meta:
        model = InternshipApplication
        fields = '__all__' + (
            'candidate_name',
            'internship_role',
            'company_name',
            'interviewer_name',
        )
        read_only_fields = ['user', 'applied_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.read_only_fields:
                field.required = False

