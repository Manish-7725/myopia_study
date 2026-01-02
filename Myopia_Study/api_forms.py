from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Student, ClinicalVisit


from django.utils.timezone import localdate

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_dashboard_overview(request):
    today = localdate()

    total_students = Student.objects.count()
    total_visits = ClinicalVisit.objects.count()

    baseline_count = ClinicalVisit.objects.filter(
        visit_type="BASELINE"
    ).count()

    followup_count = ClinicalVisit.objects.filter(
        visit_type="FOLLOW_UP"
    ).count()

    today_entries = ClinicalVisit.objects.filter(
        created_at__date=today
    ).count()

    return Response({
        "total_students": total_students,
        "total_visits": total_visits,
        "baseline_count": baseline_count,
        "followup_count": followup_count,
        "today_entries": today_entries,
    })



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_myopia_form(request):
    """
    BASELINE submission
    - Creates Student (if not exists)
    - Creates BASELINE ClinicalVisit
    - Inserts A–F data ONCE
    """

    visit_date = data.get("visit_date")

    if not visit_date:
    return Response(
        {"error": "visit_date is required"},
        status=status.HTTP_400_BAD_REQUEST
    )



    with transaction.atomic():

        # 1️⃣ Create or get student
        student = Student.objects.create(
    name=data.get("name"),
    age=data.get("age"),
    gender=data.get("gender"),
    school_name=data.get("school_name"),
)


        # 🚫 Prevent duplicate baseline
        if ClinicalVisit.objects.filter(
            student=student, visit_type="BASELINE"
        ).exists():
            return Response(
                {"error": "Baseline already exists for this student"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ Create BASELINE visit
        visit = ClinicalVisit.objects.create(
            student=student,
            visit_date=visit_date,
            visit_type="BASELINE"
        )

        # 3️⃣ Section B – Lifestyle
        LifestyleBehavior.objects.create(
            visit=visit,
            **data.get("lifestyle", {})
        )

        # 4️⃣ Section C – Environmental
        EnvironmentalFactor.objects.create(
            visit=visit,
            **data.get("environment", {})
        )

        # 5️⃣ Section D – Clinical history
        ClinicalHistory.objects.create(
            visit=visit,
            **data.get("history", {})
        )

        # 6️⃣ Section E – Awareness
        AwarenessSafety.objects.create(
            visit=visit,
            **data.get("awareness", {})
        )

        # 7️⃣ Section F – Ocular exam
        OcularExamination.objects.create(
            visit=visit,
            **data.get("ocular", {})
        )

    return Response(
        {
            "message": "Baseline submitted successfully",
            "student_id": student.student_id,
            "visit_date": visit.visit_date,
            "visit_type": visit.visit_type
        },
        status=status.HTTP_201_CREATED
    )
