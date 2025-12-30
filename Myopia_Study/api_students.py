from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAdmin
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

@api_view(["GET", "POST"])
@permission_classes([IsAdmin])
def students_api(request):

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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_students(request):
    """
    Return students created by the logged-in user
    """
    students = (
        Student.objects
        .filter(created_by=request.user)
        .order_by("-created_at")
    )

    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
