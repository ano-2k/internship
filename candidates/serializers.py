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
        

