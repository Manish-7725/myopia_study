# from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



class Student(models.Model):
    """
    Table A: Student Demographics (Master Table)
    Created once per student.
    """
    student_id = models.CharField(max_length=50, unique=True)

    name = models.CharField(max_length=100)

    school_name = models.CharField(
    max_length=150,
    blank=True,
    db_index=True
)

    # date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField()

    gender = models.CharField(max_length=10)

    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    father_myopia = models.BooleanField(default=False)
    mother_myopia = models.BooleanField(default=False)
    
    number_of_siblings = models.PositiveIntegerField(
    null=True, blank=True,
    verbose_name="Number of siblings")


    BIRTH_ORDER_CHOICES = [
    ("First", "First-born"),
    ("Middle", "Middle-born"),
    ("Last", "Last-born"),
    ("Only", "Only child"),
]

    birth_order = models.CharField(
    max_length=10,
    choices=BIRTH_ORDER_CHOICES,
    null=True, blank=True,
    verbose_name="Birth order"
    )

    sibling_details = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Section A: Student Demographics"

    def __str__(self):
        return f"{self.student_id} - {self.name}"
    


class VisitBase(models.Model):
    """
    Abstract base for all visit-based tables (B-E)
    """
    student = models.ForeignKey(
    Student,
    on_delete=models.CASCADE,
    related_name="%(class)s_records"
)

    visit_date = models.DateField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True



class LifestyleBehavior(VisitBase):

    # 10. Time of daily outdoor activity
    outdoor_time_start = models.TimeField(null=True, blank=True)

    # 11. Duration of outdoor activities
    outdoor_duration = models.CharField(
        max_length=20,
        choices=[
            ("<1 hr", "<1 hr"),
            ("1-2 hrs", "1-2 hrs"),
            ("2-4 hrs", "2-4 hrs"),
            (">4 hrs", ">4 hrs"),
        ]
    )

    # 12. Daily sun exposure
    sun_exposure = models.CharField(
        max_length=20,
        choices=[
            ("<15 min", "<15 min"),
            ("15-30 min", "15-30 min"),
            ("30-60 min", "30-60 min"),
            (">1 hr", ">1 hr"),
        ]
    )

    # 13. Near work hours
    near_work_hours = models.CharField(
        max_length=20,
        choices=[
            ("<2 hrs", "<2 hrs"),
            ("2-4 hrs", "2-4 hrs"),
            ("4-6 hrs", "4-6 hrs"),
            (">6 hrs", ">6 hrs"),
        ]
    )

    # 14. Screen time
    screen_time = models.CharField(
        max_length=20,
        choices=[
            ("<1 hr", "<1 hr"),
            ("1-3 hrs", "1-3 hrs"),
            ("3-5 hrs", "3-5 hrs"),
            (">5 hrs", ">5 hrs"),
        ]
    )

    # 15. Device used (SINGLE value)
    primary_device = models.CharField(
        max_length=20,
        choices=[
            ("TV", "TV"),
            ("Tablet", "Tablet"),
            ("Mobile", "Mobile"),
            ("Laptop", "Laptop/Desktop"),
        ]
    )

    # 16. Reading distance
    reading_distance = models.CharField(
        max_length=20,
        choices=[
            ("<20 cm", "<20 cm"),
            ("20-30 cm", "20-30 cm"),
            (">30 cm", ">30 cm"),
        ]
    )

    # 17. Viewing posture ratio
    viewing_posture_ratio = models.CharField(
        max_length=10,
        choices=[
            ("Low", "Low"),
            ("High", "High"),
            ("Optimum", "Optimum"),
        ]
    )

    # 18. Dietary habits (SINGLE choice)
    dietary_habit = models.CharField(
        max_length=20,
        choices=[
            ("Balanced", "Balanced"),
            ("Junk", "Junk food-dominant"),
            ("Vegetarian", "Vegetarian"),
            ("NonVegetarian", "Non-vegetarian"),
            ("Other", "Other"),
        ]
    )

    dietary_other = models.CharField(max_length=100, blank=True)

    # 19. Sleep duration
    sleep_duration = models.CharField(
        max_length=20,
        choices=[
            ("<6 hrs", "<6 hrs"),
            ("6-7 hrs", "6-7 hrs"),
            ("7-8 hrs", "7-8 hrs"),
            (">8 hrs", ">8 hrs"),
        ]
    )

    # 20. Usual bedtime
    usual_bedtime = models.CharField(
        max_length=10,
        choices=[
            ("Before9", "Before 9 PM"),
            ("9-10", "9-10 PM"),
            ("10-11", "10-11 PM"),
            ("After11", "After 11 PM"),
        ]
    )


    class Meta:
        verbose_name = "Section B: Lifestyle"


class EnvironmentalFactor(VisitBase):

    school_type = models.CharField(
        max_length=20,
        choices=[
            ("Urban", "Urban"),
            ("Rural", "Rural"),
        ]
    )

    classroom_strength = models.CharField(
        max_length=20,
        choices=[
            ("Small", "<30"),
            ("Moderate", "30–50"),
            ("High", ">50"),
        ]
    )

    seating_position = models.CharField(
        max_length=20,
        choices=[
            ("Front", "Front"),
            ("Middle", "Middle"),
            ("Back", "Back"),
        ]
    )

    teaching_methodology = models.CharField(
        max_length=20,
        choices=[
            ("Digital", "Digital (projectors/screens)"),
            ("Traditional", "Traditional (blackboard/books)"),
        ]
    )

    lighting = models.CharField(
        max_length=20,
        choices=[
            ("Dim", "Dim"),
            ("Adequate", "Adequate"),
            ("Bright", "Bright"),
        ]
    )

    sunlight_source = models.CharField(
        max_length=20,
        choices=[
            ("Natural", "Natural"),
            ("Artificial", "Artificial"),
            ("Both", "Both"),
        ]
    )

    class Meta:
        verbose_name = "Section C: Environment"



class ClinicalHistory(VisitBase):

    # 28. Prior diagnosis
    diagnosed_earlier = models.BooleanField(
        verbose_name="Diagnosed with myopia earlier?"
    )

    # 29. Age at diagnosis (only if yes)
    age_at_diagnosis = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Age at diagnosis (years)"
    )

    # 30. Change in last 3 years
    power_changed_last_3yrs = models.BooleanField(
        verbose_name="Spectacle power changed in last 3 years?"
    )

    # 31. Compliance
    compliance = models.CharField(
        max_length=20,
        choices=[
            ("Always", "Always"),
            ("Sometimes", "Sometimes"),
            ("Rarely", "Rarely"),
        ]
    )

    # 32. Previous prescription
    previous_re = models.CharField(
        max_length=20,
        blank=True
    )
    previous_le = models.CharField(
        max_length=20,
        blank=True
    )

    # Current prescription
    current_re = models.CharField(
        max_length=20,
        blank=True
    )
    current_le = models.CharField(
        max_length=20,
        blank=True
    )

    class Meta:
        verbose_name = "Section D: Clinical History"



class AwarenessSafety(VisitBase):

    # Aware of symptoms
    aware_eye_strain = models.BooleanField(
        verbose_name="Aware of eye strain symptoms?"
    )

# Access to Vision Care
    access_to_vision_care = models.BooleanField(
        verbose_name="Access to vision care in your area?"
    )

    # Preventive measures
    follows_preventive_measures = models.CharField(
        max_length=20,
        choices=[
            ("Always", "Always"),
            ("Sometimes", "Sometimes"),
            ("Never", "Never"),
        ]
    )

    # Source of awareness (comma-separated)
    source_of_awareness = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated: School, Family, Doctor, Media, Other"
    )

    class Meta:
        verbose_name = "Section E: Awareness & Safety"


class OcularExamination(VisitBase):

    # 36. UCVA
    ucva_re = models.CharField(max_length=20, blank=True)
    ucva_le = models.CharField(max_length=20, blank=True)

    # 37. BCVA
    bcva_re = models.CharField(max_length=20, blank=True)
    bcva_le = models.CharField(max_length=20, blank=True)

    # 38. Cycloplegic auto-refraction (SE)
    cyclo_se_re = models.CharField(max_length=20, blank=True)
    cyclo_se_le = models.CharField(max_length=20, blank=True)

    # 39. Spherical power
    spherical_re = models.CharField(max_length=20, blank=True)
    spherical_le = models.CharField(max_length=20, blank=True)

    # 40. Axial length (mm)
    axial_length_re = models.CharField(max_length=20, blank=True)
    axial_length_le = models.CharField(max_length=20, blank=True)

    # 41. Corneal curvature (K readings)
    keratometry_re = models.CharField(max_length=50, blank=True)
    keratometry_le = models.CharField(max_length=50, blank=True)

    # 42. Central corneal thickness (µm)
    cct_re = models.CharField(max_length=20, blank=True)
    cct_le = models.CharField(max_length=20, blank=True)

    # 43. Anterior segment findings
    anterior_segment_re = models.TextField(blank=True)
    anterior_segment_le = models.TextField(blank=True)

    # 44. Amblyopia / strabismus
    amblyopia_or_strabismus = models.BooleanField()

    # 45. Fundus findings
    fundus_re = models.TextField(blank=True)
    fundus_le = models.TextField(blank=True)

    class Meta:
        verbose_name = "Section F: Ocular Examination"





class ClinicalExamination(models.Model):
    """
    Section F: Clinical Examination & Measurements
    Objective ophthalmic findings recorded at each visit.
    """

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="clinical_examinations"
    )

    visit_date = models.DateField(
        default=timezone.now,
        help_text="Date of clinical examination"
    )

    # ---------- VISUAL ACUITY ----------
    unaided_va_re = models.CharField(
        max_length=20, blank=True,
        verbose_name="Unaided Visual Acuity (Right Eye)"
    )
    unaided_va_le = models.CharField(
        max_length=20, blank=True,
        verbose_name="Unaided Visual Acuity (Left Eye)"
    )

    aided_va_re = models.CharField(
        max_length=20, blank=True,
        verbose_name="Aided Visual Acuity (Right Eye)"
    )
    aided_va_le = models.CharField(
        max_length=20, blank=True,
        verbose_name="Aided Visual Acuity (Left Eye)"
    )

    # ---------- REFRACTION ----------
    spherical_re = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    cylindrical_re = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    axis_re = models.PositiveIntegerField(null=True, blank=True)

    spherical_le = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    cylindrical_le = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    axis_le = models.PositiveIntegerField(null=True, blank=True)

    # ---------- BIOMETRY ----------
    axial_length_re = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        verbose_name="Axial Length Right Eye (mm)"
    )
    axial_length_le = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        verbose_name="Axial Length Left Eye (mm)"
    )

    # ---------- ASSESSMENT ----------
    progression_noted = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Section F: Clinical Examination"
        ordering = ["-visit_date"]

    def __str__(self):
        return f"{self.student.student_id} | Exam | {self.visit_date}"
    


class FollowUp(models.Model):

    STATUS_CHOICES = [
        ("Due", "Due"),
        ("Overdue", "Overdue"),
        ("Completed", "Completed"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="followups"
    )

    last_visit_date = models.DateField()
    next_visit_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Due"
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["next_visit_date"]

    def __str__(self):
        return f"{self.student.name} → {self.next_visit_date}"


