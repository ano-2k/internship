from django.db import models
from django.conf import settings

class Internship(models.Model):
    INTERNSHIP_TYPE_CHOICES = [
        ('in_office', 'In-Office'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote')
    ]

    FIELD_CHOICES = [
        ('accounts', 'Accounts'),
        ('administration', 'Administration'),
        ('chemical', 'Chemical'),
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('banking', 'Banking'),
        ('healthcare', 'Healthcare'),
        ('human_resource', 'Human Resource'),
        ('education', 'Education'),
        ('engineering', 'Engineering'),
        ('retail', 'Retail'),
        ('marketing', 'Marketing'),
        ('hospitality', 'Hospitality'),
        ('consulting', 'Consulting'),
        ('manufacturing', 'Manufacturing'),
        ('media', 'Media'),
        ('transportation', 'Transportation'),
        ('telecommunications', 'Telecommunications'),
        ('nonprofit', 'Nonprofit'),
        ('activate_windows', 'Activate Windows')  # Unusual, but per your list
    ]

    NATURE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ]

    DEGREE_CHOICES = [
        ('engineering', 'Engineering'),
        ('arts', 'Arts')
    ]

    company_name = models.CharField(max_length=255)
    internship_role = models.CharField(max_length=255)
    internship_type = models.CharField(max_length=20, choices=INTERNSHIP_TYPE_CHOICES)
    internship_field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    internship_nature = models.CharField(max_length=20, choices=NATURE_CHOICES)
    internship_description = models.TextField()
    required_skills = models.CharField(max_length=255)  # e.g. comma-separated "python,java"
    duration_months = models.PositiveIntegerField()
    application_start_date = models.DateField()
    application_end_date = models.DateField()
    stipend = models.CharField(max_length=50)
    eligibility_criteria = models.TextField()
    degrees_preferred = models.CharField(max_length=100)  # Store as comma-separated values if multiple
    contact_email = models.EmailField()
    contact_mobile_number = models.CharField(max_length=15)
    company_information = models.TextField()
    internship_responsibilities = models.TextField()
    total_vacancies = models.PositiveIntegerField(default=1)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='internships')
    created_at = models.DateTimeField(auto_now_add=True)


class FaceToFaceInterview(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)  # Link to User who owns it
    internship_role = models.CharField(max_length=255)
    date = models.DateField()
    zoom = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.internship_role} on {self.date}"
    
    