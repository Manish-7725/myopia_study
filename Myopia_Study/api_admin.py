from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.utils.timezone import now, timedelta
import pandas as pd
from .models import Student, ClinicalVisit
from .serializers import StudentSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_overview(request):
    today = now().date()
    return Response({
        "total_students": Student.objects.count(),
        "total_followups": ClinicalVisit.objects.filter(visit_type="FOLLOW_UP").count(),
        "due_this_week": ClinicalVisit.objects.filter(visit_type="FOLLOW_UP", visit_date__range=[today, today + timedelta(days=7)]).count(),
        "missed_followups": ClinicalVisit.objects.filter(visit_type="FOLLOW_UP", visit_date__lt=today).count(),
    })

from rest_framework import viewsets
from .serializers import SignupSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        role = request.data.get("role")
        if role == 'Admin':
            user.is_staff = True
            user.save()

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUser])
def admin_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == "PUT":
        # Admin overrides or other user property updates
        serializer = UserSerializer(user, data=request.data, partial=True) # Use partial=True for PATCH-like behavior
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def admin_reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    new_password = request.data.get("new_password")

    if not new_password:
        return Response({"error": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # validate_password(new_password, user) # Optional: Django's password validators
        user.set_password(new_password)
        user.save()
        # Invalidate all sessions for the user to force logout
        update_session_auth_hash(request, user) 
        return Response({"message": "Password reset successfully and user sessions invalidated."})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def admin_force_logout(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Invalidate all sessions for the user to force logout
    update_session_auth_hash(request, user)
    return Response({"message": "User force logged out successfully (sessions invalidated)."})

@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_students_list(request):
    qs = Student.objects.all().order_by("-created_at")
    
    # Filters
    q = request.GET.get("q")
    if q: qs = qs.filter(Q(name__icontains=q) | Q(student_id__icontains=q) | Q(school_name__icontains=q))
    
    gender = request.GET.get("gender")
    if gender: qs = qs.filter(gender__iexact=gender)

    school = request.GET.get("school")
    if school: qs = qs.filter(school_name__icontains=school)

    from_date = request.GET.get("from_date")
    if from_date: qs = qs.filter(created_at__date__gte=from_date)

    to_date = request.GET.get("to_date")
    if to_date: qs = qs.filter(created_at__date__lte=to_date)

    paginator = PageNumberPagination()
    paginator.page_size = 10
    result = paginator.paginate_queryset(qs, request)
    return paginator.get_paginated_response(StudentSerializer(result, many=True).data)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUser])
def admin_student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == "DELETE":
        student.delete()
        return Response(status=204)
    if request.method == "PUT":
        student.name = request.data.get("name", student.name)
        student.age = request.data.get("age", student.age)
        student.school_name = request.data.get("school", student.school_name)
        student.gender = request.data.get("gender", student.gender)
        student.save()
        return Response({"message": "Updated"})
    
    # Get Profile with Timeline
    visits = ClinicalVisit.objects.filter(student=student).order_by('visit_date')
    data = StudentSerializer(student).data
    data['lifestyles'] = [v.get_lifestyle for v in visits if v.get_lifestyle]
    data['ocular'] = [v.get_ocular_exam for v in visits if v.get_ocular_exam]
    return Response(data)

# High-Performance Excel Export
class ExportClinicalDataView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        visits = ClinicalVisit.objects.get_full_export_data()
        data_list = []
        for v in visits:
            row = {
                'Student_ID': v.student.student_id, 'Name': v.student.name,
                'Visit_Date': v.visit_date, 'Visit_Type': v.visit_type
            }
            if v.get_lifestyle: row.update({'Outdoor_Time': v.get_lifestyle.outdoor_time})
            if v.get_ocular_exam: row.update({'Vision_R': v.get_ocular_exam.uncorrectedvisual_acuity_right_eye})
            data_list.append(row)
        
        df = pd.DataFrame(data_list)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Study_Export.xlsx"'
        df.to_excel(response, index=False)
        return response