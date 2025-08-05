from rest_framework import serializers
from .models import CandidateProfile
from .models import InternshipApplication

class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = '__all__'
        read_only_fields = ['user']




class InternshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipApplication
        fields = '__all__'
        read_only_fields = ['user', 'applied_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional except user and applied_at (already read-only)
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.read_only_fields:
                field.required = False
        
# serializers.py

class CandidateAcceptedApplicationSerializer(serializers.ModelSerializer):
    interview_id = serializers.SerializerMethodField()
    interview_date = serializers.SerializerMethodField()
    interview_time = serializers.SerializerMethodField()
    interview_zoom = serializers.SerializerMethodField()

    class Meta:
        model = InternshipApplication
        fields = ['id', 'candidate_name', 'internship_role', 'interview_id', 'interview_date','interview_time','interview_zoom']

    def get_interview_id(self, obj):
        interview = obj.interviews.first()
        return interview.id if interview else None

    def get_interview_date(self, obj):
        interview = obj.interviews.first()
        return interview.date if interview else None
    
    def get_interview_time(self, obj):
       interview = obj.interviews.first()
       return interview.time.strftime('%H:%M') if interview and interview.time else None



    def get_interview_zoom(self, obj):
        interview = obj.interviews.first()
        return interview.zoom if interview else None


