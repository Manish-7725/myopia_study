from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils.timezone import localdate

from .models import (
    Student, ClinicalVisit, LifestyleBehavior, EnvironmentalFactor, 
    ClinicalHistory, AwarenessSafety, OcularExamination
)

# =====================================================
# DASHBOARD OVERVIEW API
# =====================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_dashboard_overview(request):
    """
    Provides aggregated metrics for the User Dashboard.
    """
    today = localdate()

    return Response({
        "total_visits": ClinicalVisit.objects.count(),
        "total_students": Student.objects.count(),
        
        # Entries created today
        "today_entries": ClinicalVisit.objects.filter(
            created_at__date=today
        ).count(),

        # Follow-up stats
        "followup_count": ClinicalVisit.objects.filter(visit_type="FOLLOW_UP").count(),
        
        "pending_count": ClinicalVisit.objects.filter(
            visit_type="FOLLOW_UP",
            visit_date__gt=today  # Future visits
        ).count(),
        
        "overdue_count": ClinicalVisit.objects.filter(
            visit_type="FOLLOW_UP",
            visit_date__lt=today  # Past visits
        ).count()
    })


# =====================================================
# 1. BASELINE FORM SUBMISSION
# =====================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_student_form(request):
    data = request.data
    visit_date = data.get("visit_date")
    visit_type = "BASELINE"

    if not visit_date:
        return Response({"error": "visit_date is required"}, status=status.HTTP_400_BAD_REQUEST)

    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")

    if not all([name, age, gender]):
        return Response({"error": "Name, age, and gender are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Prevent duplicate students
    if Student.objects.filter(name=name, age=age, gender=gender).exists():
        return Response(
            {"error": "A student with this name, age, and gender already exists."},
            status=status.HTTP_409_CONFLICT
        )

    try:
        with transaction.atomic():
            # A. Create Student
            student = Student.objects.create(
                name=name,
                age=age,
                gender=gender,
                school_name=data.get("school_name"),
                height=data.get("height"),
                weight=data.get("weight"),
                parental_myopia=data.get("parental_myopia"),
                num_siblings=data.get("num_siblings"),
                birth_order=data.get("birth_order"),
                siblings_myopia=data.get("siblings_myopia")
            )

            # B. Create Visit
            visit = ClinicalVisit.objects.create(
                student=student,
                visit_date=visit_date,
                visit_type=visit_type
            )

            # C. Create All Sections (Mandatory for Baseline)
            # We use .get({}, {}) to default to empty dicts if missing, 
            # effectively creating rows with null values (which is fine for baseline)
            LifestyleBehavior.objects.create(visit=visit, **data.get("lifestyle", {}))
            EnvironmentalFactor.objects.create(visit=visit, **data.get("environment", {}))
            ClinicalHistory.objects.create(visit=visit, **data.get("history", {}))
            AwarenessSafety.objects.create(visit=visit, **data.get("awareness", {}))
            OcularExamination.objects.create(visit=visit, **data.get("ocular", {}))

        return Response({
            "message": "Baseline submitted successfully",
            "student_id": student.student_id,
            "status": "success"
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# 2. FOLLOW-UP SUBMISSION (OPTIMIZED)
# =====================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_followup_form(request):
    data = request.data
    student_id = data.get("student_id")
    visit_date = data.get("visit_date")

    if not student_id or not visit_date:
        return Response({"error": "student_id and visit_date are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        with transaction.atomic():
            # A. Create Visit
            visit = ClinicalVisit.objects.create(
                student=student,
                visit_date=visit_date,
                visit_type="FOLLOW_UP"
            )

            # B. Create Related Sections ONLY IF DATA EXISTS
            # This prevents creating empty rows in your database
            
            if data.get("lifestyle"):
                LifestyleBehavior.objects.create(visit=visit, **data.get("lifestyle"))
            
            if data.get("environment"):
                EnvironmentalFactor.objects.create(visit=visit, **data.get("environment"))
                
            if data.get("history"):
                ClinicalHistory.objects.create(visit=visit, **data.get("history"))
                
            if data.get("awareness"):
                AwarenessSafety.objects.create(visit=visit, **data.get("awareness"))

            # Section F is usually mandatory, but we check anyway
            if data.get("ocular"):
                OcularExamination.objects.create(visit=visit, **data.get("ocular"))

        return Response({
            "message": "Follow-up submitted successfully",
            "student_id": student.student_id,
            "visit_id": visit.id,
            "status": "success"
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)