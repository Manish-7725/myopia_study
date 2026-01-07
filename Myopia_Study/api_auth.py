# Myopia_Study/api_auth.py

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer

User = get_user_model()


# =====================================================
# HELPERS
# =====================================================

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# =====================================================
# SIGNUP
# =====================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def signup_api(request):
    serializer = SignupSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()

    return Response(
        {"message": "Signup successful"},
        status=status.HTTP_201_CREATED
    )


# =====================================================
# LOGIN (USERNAME OR EMAIL)
# =====================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(request):
    identifier = request.data.get("username")
    password = request.data.get("password")

    if not identifier or not password:
        return Response(
            {"error": "Username/Email and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = None

    # 1️⃣ Try username
    user = authenticate(username=identifier, password=password)

    # 2️⃣ Try email → username
    if user is None:
        try:
            user_obj = User.objects.get(email__iexact=identifier)
            user = authenticate(
                username=user_obj.username,
                password=password
            )
        except User.DoesNotExist:
            pass

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    tokens = get_tokens_for_user(user)

    return Response({
        "message": "Login successful",
        **tokens,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": "admin" if user.is_staff else "user",
        }
    })


# =====================================================
# USER PROFILE (VIEW / UPDATE)
# =====================================================

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    # ------------------ GET PROFILE ------------------
    if request.method == "GET":
        return Response({
            "username": user.username,
            "email": user.email,
            "role": "admin" if user.is_staff else "user",
        })

    # ------------------ UPDATE PROFILE ------------------
    data = request.data

    # Change username
    new_username = data.get("username")
    if new_username and new_username != user.username:
        if User.objects.filter(username=new_username).exists():
            return Response(
                {"error": "Username already taken"},
                status=status.HTTP_400_BAD_REQUEST
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
                status=status.HTTP_400_BAD_REQUEST
            )

    user.save()

    return Response({"message": "Profile updated successfully"})
