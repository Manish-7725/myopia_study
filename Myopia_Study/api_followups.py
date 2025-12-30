from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework import status

from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated        # ✅ ADD
from .models import FollowUp, Student
from .serializers import FollowUpCreateSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_followups(request):
    today = now().date()

    followups = FollowUp.objects.all()

    data = []
    for f in followups:
        status = "Completed"
        if f.next_visit_date >= today:
            status = "Due"
        else:
            status = "Overdue"

        data.append({
            "id": f.id,
            "student": f.student.name,
            "student_id": f.student.student_id,
            "last_visit": f.last_visit_date,
            "next_visit": f.next_visit_date,
            "status": status,
        })

    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_followup(request):
    
    student_id_str = request.data.get("student")

    try:
        if request.user.is_staff:
        # Admin: can create follow-up for any student
            student = Student.objects.get(student_id=student_id_str)
        else:
        # User: can create follow-up only for their own student
            student = Student.objects.get(
                student_id=student_id_str,
                created_by=request.user
        )
    except Student.DoesNotExist:
        return Response(
        {"detail": "Student not found or access denied"},
        status=status.HTTP_403_FORBIDDEN
    )

    
    serializer = FollowUpCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
