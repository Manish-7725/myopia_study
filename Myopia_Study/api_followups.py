from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Student, ClinicalVisit, OcularExamination
from .serializers import OcularExaminationSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_followup(request):
    """
    FOLLOW-UP API
    - Uses student_id
    - Creates NEW ClinicalVisit
    - Inserts NEW OcularExamination
    - Old data remains untouched
    """

    student_id = request.data.get("student_id")
    visit_date = request.data.get("visit_date")
    ocular_data = request.data.get("ocular")


    if not student_id or not visit_date or not ocular_data:
        return Response(
            {"error": "student_id, visit_date, and ocular data are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    with transaction.atomic():
        # 1️⃣ Create FOLLOW-UP visit
        visit = ClinicalVisit.objects.create(
            student=student,
            visit_date=visit_date,
            visit_type="FOLLOW_UP"
        )

        # 2️⃣ Insert NEW ocular examination
        serializer = OcularExaminationSerializer(data=ocular_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(visit=visit)

    return Response(
        {
            "message": "Follow-up created successfully",
            "student_id": student.student_id,
            "visit_date": visit.visit_date,
            "visit_type": visit.visit_type
        },
        status=status.HTTP_201_CREATED
    )
