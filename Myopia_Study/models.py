from django.db import models
from django.contrib.auth.models import User

# Section A: Demographic Information
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    parental_myopia = models.CharField(max_length=20, blank=True, null=True)
    num_siblings = models.PositiveSmallIntegerField(blank=True, null=True)
    birth_order = models.CharField(max_length=20, blank=True, null=True)
    siblings_myopia = models.PositiveSmallIntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Section B: Behavioral and Lifestyle Factors
class LifestyleBehavior(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="lifestyles")
    outdoor_time = models.TimeField(blank=True, null=True)
    outdoor_duration = models.CharField(max_length=20, blank=True, null=True)
    sun_exposure = models.CharField(max_length=20, blank=True, null=True)
    near_work_hours = models.CharField(max_length=20, blank=True, null=True)
    screen_time = models.CharField(max_length=20, blank=True, null=True)
    primary_device = models.CharField(max_length=20, blank=True, null=True)
    reading_distance = models.CharField(max_length=20, blank=True, null=True)
    viewing_posture_ratio = models.CharField(max_length=20, blank=True, null=True)
    dietary_habit = models.CharField(max_length=20, blank=True, null=True)
    dietary_other = models.CharField(max_length=100, blank=True, null=True)
    sleep_duration = models.CharField(max_length=20, blank=True, null=True)
    usual_bedtime = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Section C: Environmental Factors
class EnvironmentalFactor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="environments")
    school_type = models.CharField(max_length=20, blank=True, null=True)
    classroom_strength = models.CharField(max_length=20, blank=True, null=True)
    seating_position = models.CharField(max_length=20, blank=True, null=True)
    teaching_methodology = models.CharField(max_length=30, blank=True, null=True)
    lighting = models.CharField(max_length=20, blank=True, null=True)
    sunlight_source = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Section D: Myopia History
class ClinicalHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="histories")
    diagnosed_earlier = models.BooleanField(default=False)
    age_at_diagnosis = models.PositiveSmallIntegerField(blank=True, null=True)
    power_changed_last_3yrs = models.BooleanField(default=False)
    compliance = models.CharField(max_length=20, blank=True, null=True)
    previous_re = models.CharField(max_length=20, blank=True, null=True)
    previous_le = models.CharField(max_length=20, blank=True, null=True)
    current_re = models.CharField(max_length=20, blank=True, null=True)
    current_le = models.CharField(max_length=20, blank=True, null=True)
    visit_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Section E: Awareness
class AwarenessSafety(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="awareness")
    aware_eye_strain = models.BooleanField(default=False)
    access_to_vision_care = models.BooleanField(default=False)
    follows_preventive_measures = models.CharField(max_length=20, blank=True, null=True)
    source_of_awareness = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Section F: Ocular Examination
class OcularExamination(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="ocular")
    ucva_re = models.CharField(max_length=20, blank=True, null=True)
    ucva_le = models.CharField(max_length=20, blank=True, null=True)
    bcva_re = models.CharField(max_length=20, blank=True, null=True)
    bcva_le = models.CharField(max_length=20, blank=True, null=True)
    cyclo_se_re = models.CharField(max_length=20, blank=True, null=True)
    cyclo_se_le = models.CharField(max_length=20, blank=True, null=True)
    spherical_re = models.CharField(max_length=20, blank=True, null=True)
    spherical_le = models.CharField(max_length=20, blank=True, null=True)
    axial_length_re = models.CharField(max_length=20, blank=True, null=True)
    axial_length_le = models.CharField(max_length=20, blank=True, null=True)
    keratometry_re = models.CharField(max_length=20, blank=True, null=True)
    keratometry_le = models.CharField(max_length=20, blank=True, null=True)
    cct_re = models.CharField(max_length=20, blank=True, null=True)
    cct_le = models.CharField(max_length=20, blank=True, null=True)
    anterior_segment_re = models.TextField(blank=True, null=True)
    anterior_segment_le = models.TextField(blank=True, null=True)
    amblyopia_or_strabismus = models.BooleanField(default=False)
    fundus_re = models.TextField(blank=True, null=True)
    fundus_le = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# FollowUp table for follow-up records
class FollowUp(models.Model):
    STATUS_CHOICES = [
        ("due", "Due"),
        ("overdue", "Overdue"),
        ("completed", "Completed"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="followups")
    last_visit = models.DateField()
    next_visit = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="due")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FollowUp for {self.student.name} on {self.next_visit}"

# Follow-up Environmental Factors
class FollowUpEnvironmental(models.Model):
    followup = models.OneToOneField(FollowUp, on_delete=models.CASCADE, related_name="environmental")
    school_type = models.CharField(max_length=20, blank=True, null=True)
    classroom_strength = models.CharField(max_length=20, blank=True, null=True)
    seating_position = models.CharField(max_length=20, blank=True, null=True)
    teaching_methodology = models.CharField(max_length=30, blank=True, null=True)
    lighting = models.CharField(max_length=20, blank=True, null=True)
    sunlight_source = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Follow-up Myopia History
class FollowUpHistory(models.Model):
    followup = models.OneToOneField(FollowUp, on_delete=models.CASCADE, related_name="history")
    diagnosed_earlier = models.BooleanField(default=False)
    age_at_diagnosis = models.PositiveSmallIntegerField(blank=True, null=True)
    power_changed_last_3yrs = models.BooleanField(default=False)
    compliance = models.CharField(max_length=20, blank=True, null=True)
    previous_re = models.CharField(max_length=20, blank=True, null=True)
    previous_le = models.CharField(max_length=20, blank=True, null=True)
    current_re = models.CharField(max_length=20, blank=True, null=True)
    current_le = models.CharField(max_length=20, blank=True, null=True)
    visit_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Follow-up Ocular Examination
class FollowUpOcular(models.Model):
    followup = models.OneToOneField(FollowUp, on_delete=models.CASCADE, related_name="ocular")
    ucva_re = models.CharField(max_length=20, blank=True, null=True)
    ucva_le = models.CharField(max_length=20, blank=True, null=True)
    bcva_re = models.CharField(max_length=20, blank=True, null=True)
    bcva_le = models.CharField(max_length=20, blank=True, null=True)
    cyclo_se_re = models.CharField(max_length=20, blank=True, null=True)
    cyclo_se_le = models.CharField(max_length=20, blank=True, null=True)
    spherical_re = models.CharField(max_length=20, blank=True, null=True)
    spherical_le = models.CharField(max_length=20, blank=True, null=True)
    axial_length_re = models.CharField(max_length=20, blank=True, null=True)
    axial_length_le = models.CharField(max_length=20, blank=True, null=True)
    keratometry_re = models.CharField(max_length=20, blank=True, null=True)
    keratometry_le = models.CharField(max_length=20, blank=True, null=True)
    cct_re = models.CharField(max_length=20, blank=True, null=True)
    cct_le = models.CharField(max_length=20, blank=True, null=True)
    anterior_segment_re = models.TextField(blank=True, null=True)
    anterior_segment_le = models.TextField(blank=True, null=True)
    amblyopia_or_strabismus = models.BooleanField(default=False)
    fundus_re = models.TextField(blank=True, null=True)
    fundus_le = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
