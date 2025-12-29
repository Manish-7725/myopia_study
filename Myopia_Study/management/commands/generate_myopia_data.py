"""
Management command to generate 1000+ test entries for Myopia Progression Study
questionnaire and populate the PostgreSQL database.
"""

from django.core.management.base import BaseCommand
from django.db import connection
from datetime import date, timedelta
import random
from decimal import Decimal

from Myopia_Study.models import (
    Student,
    LifestyleBehavior,
    EnvironmentalFactor,
    ClinicalHistory,
    AwarenessSafety,
    OcularExamination,
    ClinicalExamination,
)


class Command(BaseCommand):
    help = """
    Generate 1000+ realistic test entries for Myopia Progression Study questionnaire.
    Populates PostgreSQL database with comprehensive questionnaire data.
    
    Usage: python manage.py generate_myopia_data
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--students',
            type=int,
            default=150,
            help='Number of students to create (default: 150)'
        )
        parser.add_argument(
            '--visits',
            type=int,
            default=5,
            help='Number of visits per student (default: 5)'
        )
        parser.add_argument(
            '--batch',
            type=str,
            default='',
            help='Batch identifier for unique student IDs (auto-generated if empty)'
        )

    def handle(self, *args, **options):
        import time
        import uuid
        
        num_students = options['students']
        visits_per_student = options['visits']
        batch_id = options['batch'] or str(int(time.time()))  # Use timestamp if not provided

        self.stdout.write(
            self.style.SUCCESS("\n" + "=" * 80)
        )
        self.stdout.write(
            self.style.SUCCESS("MYOPIA PROGRESSION STUDY - QUESTIONNAIRE DATA GENERATION")
        )
        self.stdout.write(
            self.style.SUCCESS("=" * 80)
        )

        self.stdout.write(f"\n📋 Generating test data with:")
        self.stdout.write(f"   • Batch ID: {batch_id}")
        self.stdout.write(f"   • Students: {num_students}")
        self.stdout.write(f"   • Visits per student: {visits_per_student}")
        self.stdout.write(f"   • Expected total entries: ~{num_students * visits_per_student * 6}\n")

        self.generate_questionnaire_data(num_students, visits_per_student, batch_id)

    def generate_questionnaire_data(self, num_students, visits_per_student, batch_id):
        """Generate realistic questionnaire data with optimized batch operations"""

        names = [
            "Aarav", "Vivaan", "Aditya", "Arjun", "Rohan", "Vikram", "Sanjay", "Nikhil",
            "Akshay", "Dev", "Ananya", "Priya", "Disha", "Riya", "Nisha", "Kavya",
            "Shreya", "Pooja", "Anjali", "Meera", "Sneha", "Isha", "Radha", "Neha"
        ]

        students_created = 0
        records_created = 0
        batch_size = 50  # Process in smaller batches

        # Create students with questionnaire data
        for batch_start in range(0, num_students, batch_size):
            batch_end = min(batch_start + batch_size, num_students)
            
            # Create students for this batch
            students = []
            for student_idx in range(batch_start, batch_end):
                student_id = f"{batch_id}_{str(student_idx + 1).zfill(4)}"
                age = random.randint(6, 18)

                students.append(
                    Student(
                        student_id=student_id,
                        name=random.choice(names),
                        age=age,
                        gender=random.choice(["Male", "Female"]),
                        height_cm=Decimal(str(round(random.uniform(110, 185), 2))),
                        weight_kg=Decimal(str(round(random.uniform(25, 90), 2))),
                        father_myopia=random.choice([True, False]),
                        mother_myopia=random.choice([True, False]),
                        number_of_siblings=random.randint(0, 4),
                        birth_order=random.choice(["First", "Middle", "Last", "Only"]),
                        sibling_details=f"Sibling data for {student_id}"
                    )
                )

            # Bulk create students
            created_students = Student.objects.bulk_create(students)
            students_created += len(created_students)

            # Create visit records for each student
            for student in created_students:
                for visit_idx in range(visits_per_student):
                    visit_date = date.today() - timedelta(days=random.randint(0, 365))

                    # Create all related records for this visit
                    try:
                        # Section B: Lifestyle Behavior
                        LifestyleBehavior.objects.create(
                            student=student,
                            visit_date=visit_date,
                            outdoor_duration=random.choice(["<1 hr", "1-2 hrs", "2-4 hrs", ">4 hrs"]),
                            sun_exposure=random.choice(["<15 min", "15-30 min", "30-60 min", ">1 hr"]),
                            near_work_hours=random.choice(["<2 hrs", "2-4 hrs", "4-6 hrs", ">6 hrs"]),
                            screen_time=random.choice(["<1 hr", "1-3 hrs", "3-5 hrs", ">5 hrs"]),
                            primary_device=random.choice(["TV", "Tablet", "Mobile", "Laptop"]),
                            reading_distance=random.choice(["<20 cm", "20-30 cm", ">30 cm"]),
                            viewing_posture_ratio=random.choice(["Low", "High", "Optimum"]),
                            dietary_habit=random.choice(["Balanced", "Junk", "Vegetarian", "NonVegetarian"]),
                            sleep_duration=random.choice(["<6 hrs", "6-7 hrs", "7-8 hrs", ">8 hrs"]),
                            usual_bedtime=random.choice(["Before9", "9-10", "10-11", "After11"])
                        )
                        records_created += 1

                        # Section C: Environmental Factors
                        EnvironmentalFactor.objects.create(
                            student=student,
                            visit_date=visit_date,
                            school_type=random.choice(["Urban", "Rural"]),
                            classroom_strength=random.choice(["Small", "Moderate", "High"]),
                            seating_position=random.choice(["Front", "Middle", "Back"]),
                            teaching_methodology=random.choice(["Digital", "Traditional"]),
                            lighting=random.choice(["Dim", "Adequate", "Bright"]),
                            sunlight_source=random.choice(["Natural", "Artificial", "Both"])
                        )
                        records_created += 1

                        # Section D: Clinical History
                        ClinicalHistory.objects.create(
                            student=student,
                            visit_date=visit_date,
                            diagnosed_earlier=random.choice([True, False]),
                            age_at_diagnosis=random.randint(4, student.age) if random.choice([True, False]) else None,
                            power_changed_last_3yrs=random.choice([True, False]),
                            compliance=random.choice(["Always", "Sometimes", "Rarely"]),
                            current_re=f"-{random.uniform(0, 8):.2f}",
                            current_le=f"-{random.uniform(0, 8):.2f}"
                        )
                        records_created += 1

                        # Section E: Awareness & Safety
                        AwarenessSafety.objects.create(
                            student=student,
                            visit_date=visit_date,
                            aware_eye_strain=random.choice([True, False]),
                            access_to_vision_care=random.choice([True, False]),
                            follows_preventive_measures=random.choice(["Always", "Sometimes", "Never"]),
                            source_of_awareness="School, Family"
                        )
                        records_created += 1

                        # Section F: Ocular Examination
                        OcularExamination.objects.create(
                            student=student,
                            visit_date=visit_date,
                            ucva_re=random.choice(["6/6", "6/9", "6/12", "6/18"]),
                            ucva_le=random.choice(["6/6", "6/9", "6/12", "6/18"]),
                            bcva_re="6/6",
                            bcva_le="6/6",
                            cyclo_se_re=f"-{random.uniform(0, 8):.2f}",
                            cyclo_se_le=f"-{random.uniform(0, 8):.2f}",
                            amblyopia_or_strabismus=False
                        )
                        records_created += 1

                        # Section F: Clinical Examination
                        ClinicalExamination.objects.create(
                            student=student,
                            visit_date=visit_date,
                            unaided_va_re=random.choice(["6/6", "6/9", "6/12"]),
                            unaided_va_le=random.choice(["6/6", "6/9", "6/12"]),
                            aided_va_re="6/6",
                            aided_va_le="6/6",
                            spherical_re=Decimal(str(round(random.uniform(-8, 0), 2))),
                            spherical_le=Decimal(str(round(random.uniform(-8, 0), 2))),
                            progression_noted=False
                        )
                        records_created += 1
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"⚠ Skipped visit for {student.student_id}: {str(e)[:50]}"))
                        continue

            # Progress indicator
            self.stdout.write(
                self.style.SUCCESS(f"✓ Processed {batch_end}/{num_students} students ({records_created} records)")
            )

        # Display final summary
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("✅ DATA GENERATION COMPLETE"))
        self.stdout.write("=" * 80)

        self.stdout.write(f"\n📊 SUMMARY:")
        self.stdout.write(f"   ✓ Students Created: {students_created}")
        self.stdout.write(f"   ✓ Total Questionnaire Records: {records_created}")
        self.stdout.write(f"\n📈 BREAKDOWN BY SECTION:")
        self.stdout.write(f"   • Section A (Demographics): {students_created}")
        self.stdout.write(f"   • Section B (Lifestyle): {students_created * visits_per_student}")
        self.stdout.write(f"   • Section C (Environment): {students_created * visits_per_student}")
        self.stdout.write(f"   • Section D (Clinical History): {students_created * visits_per_student}")
        self.stdout.write(f"   • Section E (Awareness): {students_created * visits_per_student}")
        self.stdout.write(f"   • Section F (Ocular/Clinical Exams): {students_created * visits_per_student * 2}")

        total = students_created + records_created
        self.stdout.write(f"\n🎯 TOTAL DATABASE ENTRIES: {total}")
        self.stdout.write("=" * 80 + "\n")

        self.stdout.write(
            self.style.SUCCESS("✅ All data has been saved to PostgreSQL database!")
        )
