# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from django.db.models import Q
# from django.core.paginator import Paginator
# from django.http import HttpResponse
# import csv

# from .permissions import IsAdmin
# from .models import Student, ClinicalVisit, OcularExamination
# from .serializers import OcularExaminationSerializer


# @api_view(["GET"])
# @permission_classes([IsAdmin])
# def admin_overview(request):
#     return Response({
#         "total_students": Student.objects.count(),
#         "total_visits": ClinicalVisit.objects.count(),
#         "baseline_count": ClinicalVisit.objects.filter(visit_type="BASELINE").count(),
#         "followup_count": ClinicalVisit.objects.filter(visit_type="FOLLOW_UP").count(),
#     })



# @api_view(["GET"])
# @permission_classes([IsAdmin])
# def admin_students(request):
#     qs = Student.objects.all().order_by("-created_at")

#     q = request.GET.get("q")
#     if q:
#         qs = qs.filter(
#             Q(student_id__icontains=q) |
#             Q(name__icontains=q) |
#             Q(school_name__icontains=q)
#         )

#     paginator = Paginator(qs, 50)
#     page = paginator.get_page(request.GET.get("page", 1))

#     data = []
#     for s in page:
#         visits = ClinicalVisit.objects.filter(student=s)
#         data.append({
#             "student_id": s.student_id,
#             "name": s.name,
#             "age": s.age,
#             "gender": s.gender,
#             "school_name": s.school_name,
#             "baseline_date": visits.filter(
#                 visit_type="BASELINE"
#             ).values_list("visit_date", flat=True).first(),
#             "last_visit_date": visits.order_by(
#                 "-visit_date"
#             ).values_list("visit_date", flat=True).first(),
#         })

#     return Response({
#         "count": paginator.count,
#         "results": data
#     })



# @api_view(["GET"])
# @permission_classes([IsAdmin])
# def admin_student_visits(request, student_id):
#     student = get_object_or_404(Student, student_id=student_id)

#     visits = ClinicalVisit.objects.filter(
#         student=student
#     ).order_by("visit_date")

#     return Response([
#         {
#             "visit_id": v.id,
#             "visit_date": v.visit_date,
#             "visit_type": v.visit_type,
#         }
#         for v in visits
#     ])



# @api_view(["GET", "PUT"])
# @permission_classes([IsAdmin])
# def admin_visit_ocular(request, visit_id):
#     visit = get_object_or_404(ClinicalVisit, id=visit_id)
#     ocular = get_object_or_404(OcularExamination, visit=visit)

#     if request.method == "GET":
#         return Response(OcularExaminationSerializer(ocular).data)

#     if request.method == "PUT":
#         serializer = OcularExaminationSerializer(
#             ocular,
#             data=request.data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"message": "Ocular data updated"})



# @api_view(["GET"])
# @permission_classes([IsAdmin])
# def export_visits_csv(request):
#     response = HttpResponse(content_type="text/csv")
#     response["Content-Disposition"] = 'attachment; filename="visits.csv"'

#     writer = csv.writer(response)
#     writer.writerow(["Student ID", "Visit Date", "Visit Type", "UCVA RE", "UCVA LE"])

#     visits = ClinicalVisit.objects.select_related("student")

#     for v in visits:
#         ocular = getattr(v, "ocular_exam", None)
#         writer.writerow([
#             v.student.student_id,
#             v.visit_date,
#             v.visit_type,
#             getattr(ocular, "uncorrectedvisual_acuity_right_eye", ""),
#             getattr(ocular, "uncorrectedvisual_acuity_left_eye", ""),
#         ])

#     return response
