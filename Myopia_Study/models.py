from django.db import models
from django.contrib.auth.models import User

# Section A: Demographic Information
class Student(models.Model):
    student_id = models.CharField(
        max_length=20, unique=True, db_index=True, editable=False
    )
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

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            last = Student.objects.order_by("-id").first()
            next_id = (last.id + 1) if last else 1
            self.student_id = f"STU-{next_id:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.student_id


class ClinicalVisit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    visit_date = models.DateField()  # ← date collected
    visit_type = models.CharField(
        max_length=15,
        choices=[("BASELINE", "Baseline"), ("FOLLOW_UP", "Follow-up")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student"],
                condition=models.Q(visit_type="BASELINE"),
                name="one_baseline_per_student"
            )
        ]


# Section B: Behavioral and Lifestyle Factors
class LifestyleBehavior(models.Model):
    visit = models.OneToOneField(ClinicalVisit, on_delete=models.CASCADE)
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
    visit = models.OneToOneField(ClinicalVisit, on_delete=models.CASCADE)
    school_type = models.CharField(max_length=20, blank=True, null=True)
    classroom_strength = models.CharField(max_length=20, blank=True, null=True)
    seating_position = models.CharField(max_length=20, blank=True, null=True)
    teaching_methodology = models.CharField(max_length=30, blank=True, null=True)
    lighting = models.CharField(max_length=20, blank=True, null=True)
    sunlight_source = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

# Section D: Myopia History
class ClinicalHistory(models.Model):
    visit = models.OneToOneField(ClinicalVisit, on_delete=models.CASCADE)

    diagnosed_earlier = models.BooleanField(default=False)
    age_at_diagnosis = models.PositiveSmallIntegerField(blank=True, null=True)
    power_changed_last_3yrs = models.BooleanField(default=False)
    compliance = models.CharField(max_length=20, blank=True, null=True)
    previous_re = models.CharField(max_length=20, blank=True, null=True)
    previous_le = models.CharField(max_length=20, blank=True, null=True)
    current_re = models.CharField(max_length=20, blank=True, null=True)
    current_le = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

# Section E: Awareness
class AwarenessSafety(models.Model):
    visit = models.OneToOneField(ClinicalVisit, on_delete=models.CASCADE)

    aware_eye_strain = models.BooleanField(default=False)
    access_to_vision_care = models.BooleanField(default=False)
    follows_preventive_measures = models.CharField(max_length=20, blank=True, null=True)
    source_of_awareness = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

# Section F: Ocular Examination
class OcularExamination(models.Model):
    visit = models.OneToOneField(ClinicalVisit, on_delete=models.CASCADE)

    uncorrectedvisual_acuity_right_eye = models.CharField(max_length=20, blank=True, null=True)
    uncorrectedvisual_acuity_left_eye = models.CharField(max_length=20, blank=True, null=True)

    bestcorrectedvisual_acuity_right_eye = models.CharField(max_length=20, blank=True, null=True)
    bestcorrectedvisual_acuity_left_eye = models.CharField(max_length=20, blank=True, null=True)

    cycloplegic_auto_refraction_right_eye = models.CharField(max_length=20, blank=True, null=True)
    cycloplegic_auto_refraction_left_eye = models.CharField(max_length=20, blank=True, null=True)

    spherical_power_right_eye = models.CharField(max_length=20, blank=True, null=True)
    spherical_power_left_eye = models.CharField(max_length=20, blank=True, null=True)

    axial_length_right_eye = models.CharField(max_length=20, blank=True, null=True)
    axial_length_left_eye = models.CharField(max_length=20, blank=True, null=True)

    corneal_curvature_right_eye = models.CharField(max_length=20, blank=True, null=True)
    corneal_curvature_left_eye = models.CharField(max_length=20, blank=True, null=True)

    central_corneal_thickness_right_eye = models.CharField(max_length=20, blank=True, null=True)
    central_corneal_thickness_left_eye = models.CharField(max_length=20, blank=True, null=True)

    anterior_segment_finding_right_eye = models.TextField(blank=True, null=True)
    anterior_segment_finding_left_eye = models.TextField(blank=True, null=True)

    amblyopia_or_strabismus = models.BooleanField(default=False)

    fundus_examination_finding_right_eye = models.TextField(blank=True, null=True)
    fundus_examination_finding_left_eye = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
