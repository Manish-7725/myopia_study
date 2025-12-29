from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
# from datetime import timedelta
from datetime import date, timedelta
from .models import Student, LifestyleBehavior
from .models import *
from .models import EnvironmentalFactor
from .models import AwarenessSafety
from .models import OcularExamination
from .models import FollowUp
from .models import ClinicalHistory
from .serializers import (
    MyopiaVisitSubmissionSerializer,
    StudentSerializer,
    LifestyleBehaviorSerializer,
    EnvironmentalFactorSerializer,
    ClinicalHistorySerializer,
    AwarenessSafetySerializer,
    OcularExaminationSerializer
)
from .models import Student



from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import ClinicalHistory
from .serializers import UserFormsListSerializer

class UserFormsList(ListAPIView):
    serializer_class = UserFormsListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ClinicalHistory.objects.filter(
            created_by=self.request.user
        ).order_by("-created_at")



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_myopia_form(request):
    serializer = MyopiaVisitSubmissionSerializer(data=request.data)
    if not serializer.is_valid():
        print(serializer.errors)
        return Response(serializer.errors, status=400)

    data = serializer.validated_data

    with transaction.atomic():
        # --- Section A ---
        student_data = data["student"]
        student, _ = Student.objects.get_or_create(
            student_id=student_data["student_id"],
            defaults=student_data
        )

        visit_date = date.today()

        # --- Sections B–F ---
        LifestyleBehavior.objects.create(
            student=student, visit_date=visit_date, **data["lifestyle"]
        )

        
        EnvironmentalFactor.objects.create(
            student=student, visit_date=visit_date, **data["environment"]
        )


        ClinicalHistory.objects.create(
        student=student,
            visit_date=visit_date,
            **data["history"]
        )

        AwarenessSafety.objects.create(
        student=student,
            visit_date=visit_date,
            **data["awareness"]
)
        
        OcularExamination.objects.create(
        student=student,
        visit_date=visit_date,
        **data["ocular"]
    )

        FollowUp.objects.create(
            student=student,
            last_visit_date=visit_date,
            next_visit_date=visit_date + timedelta(days=90),  # 3 months
        )


    return Response({
        "message": "Form submitted successfully",
        "student_id": student.student_id
    })

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import date

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_dashboard_overview(request):
    today = date.today()

    total_submissions = ClinicalHistory.objects.filter(
        created_by=request.user
    ).count()

    today_entries = ClinicalHistory.objects.filter(
        created_by=request.user,
        created_at__date=today
    ).count()

    pending_submissions = FollowUp.objects.filter(
        student__created_by=request.user,
        next_visit_date__gte=today
    ).count()

    return Response({
        "username": request.user.username,
        "total_submissions": total_submissions,
        "today_entries": today_entries,
        "pending_submissions": pending_submissions
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_form_detail(request, student_id, visit_date):
    try:
        student = Student.objects.get(student_id=student_id)

        data = {
            "student": StudentSerializer(student).data,
            "lifestyle": LifestyleBehaviorSerializer(
                LifestyleBehavior.objects.get(student=student, visit_date=visit_date)
            ).data,
            "environment": EnvironmentalFactorSerializer(
                EnvironmentalFactor.objects.get(student=student, visit_date=visit_date)
            ).data,
            "history": ClinicalHistorySerializer(
                ClinicalHistory.objects.get(student=student, visit_date=visit_date)
            ).data,
            "awareness": AwarenessSafetySerializer(
                AwarenessSafety.objects.get(student=student, visit_date=visit_date)
            ).data,
            "ocular": OcularExaminationSerializer(
                OcularExamination.objects.get(student=student, visit_date=visit_date)
            ).data,
        }

        

        return Response(data)

    except Exception:
        return Response({"error": "Form not found"}, status=404)




