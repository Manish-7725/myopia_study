from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer
from django.contrib.auth.models import User


# SIGNUP API
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Signup successful"},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LOGIN API
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    identifier = request.data.get("username")  # username OR email
    password = request.data.get("password")

    if not identifier or not password:
        return Response(
            {"error": "Username/Email and password required"},
            status=400
        )

    user = None

    # 1️⃣ Try username
    user = authenticate(username=identifier, password=password)

    # 2️⃣ If not found, try email → username
    if user is None:
        try:
            user_obj = User.objects.get(email__iexact=identifier)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass

    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": "admin" if user.is_staff else "user"
        }
    })



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    # ------------------ VIEW PROFILE ------------------
    if request.method == "GET":
        return Response({
            "username": user.username,
            "email": user.email,
        })

    # ------------------ UPDATE PROFILE ------------------
    if request.method == "PUT":
        data = request.data

        # Change username
        new_username = data.get("username")
        if new_username and new_username != user.username:
            if user.__class__.objects.filter(username=new_username).exists():
                return Response(
                    {"error": "Username already taken"},
                    status=400
                )
            user.username = new_username

        # Change password
        new_password = data.get("password")
        if new_password:
            try:
                validate_password(new_password, user)
                user.set_password(new_password)
            except ValidationError as e:
                return Response(
                    {"error": e.messages},
                    status=400
                )

        user.save()

        return Response({"message": "Profile updated successfully"})
