from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializers import StudentSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def students_api(request):
    # ADMIN ONLY
    if not request.user.is_staff:
        return Response({"error": "Admins only"}, status=403)

    if request.method == "GET":
        students = Student.objects.all().order_by("-created_at")
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
