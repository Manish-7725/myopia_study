
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils.timezone import localdate
from .models import Student, ClinicalVisit

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_students(request):
    students = Student.objects.filter(name__isnull=False, age__isnull=False).order_by("-created_at")
    data = []
    for s in students:
        visits = ClinicalVisit.objects.filter(student=s)
        data.append({
            "student_id": s.student_id,
            "name": s.name,
            "school_name": s.school_name or "",
            "age": s.age,
            "gender": s.gender,
            "last_visit": visits.order_by("-visit_date").values_list("visit_date", flat=True).first() or "No visits",
        })

    paginator = PageNumberPagination()
    paginator.page_size = 10
    result = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(result)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_student_visits(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    visits = ClinicalVisit.objects.filter(student=student).order_by("-visit_date")
    return Response([{
        "visit_date": v.visit_date,
        "visit_type": v.visit_type,
    } for v in visits])

@api_view(["GET"])
def user_forms(request):
    visits = ClinicalVisit.objects.filter(visit_type="BASELINE").order_by("-visit_date")
    data = []
    for v in visits:
        data.append({
            "id": v.student.student_id,  # Changed to match JS expectation
            "visit_date": v.visit_date,  # Changed to match JS expectation
            "name": v.student.name or "Unknown",  # Changed to match JS expectation
            "school_name": v.student.school_name or "",
            "status": "Completed",
        })

    paginator = PageNumberPagination()
    paginator.page_size = 10
    result = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(result)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_recent_activity(request):
    visits = ClinicalVisit.objects.all().order_by("-visit_date")[:20]
    data = []
    for v in visits:
        data.append({
            "student_name": v.student.name or "Unknown",
            "activity": "New Clinical Entry" if v.visit_type == "BASELINE" else "Follow-up",
            "date": v.visit_date,
            "action_text": "View Entry",
        })
    return Response(data)  # Recent activity doesn't need pagination as it's limited to 20 items

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_followups(request):
    today = localdate()
    visits = ClinicalVisit.objects.filter(visit_type="FOLLOW_UP").order_by("-visit_date")
    data = []
    for v in visits:
        status = "Completed"
        if v.visit_date > today:
            status = "Due"
        elif v.visit_date < today:
            status = "Overdue"

        data.append({
            "student_id": v.student.student_id,
            "student_name": v.student.name,
            "school_name": v.student.school_name,
            "last_visit": v.visit_date,
            "status": status,
        })

    paginator = PageNumberPagination()
    paginator.page_size = 10
    result = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(result)
