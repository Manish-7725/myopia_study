from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import (
    Student, ClinicalVisit, LifestyleBehavior, EnvironmentalFactor,
    ClinicalHistory, AwarenessSafety, OcularExamination
)

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ("username", "email", "password")
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "email", "role", "date_joined", "last_login")

    def get_role(self, obj):
        return "Admin" if obj.is_staff else "User"

# --- Sub-Section Serializers ---
class LifestyleBehaviorSerializer(serializers.ModelSerializer):
    class Meta: model = LifestyleBehavior; exclude = ["visit", "created_at"]
class EnvironmentalFactorSerializer(serializers.ModelSerializer):
    class Meta: model = EnvironmentalFactor; exclude = ["visit", "created_at"]
class ClinicalHistorySerializer(serializers.ModelSerializer):
    class Meta: model = ClinicalHistory; exclude = ["visit", "created_at"]
class AwarenessSafetySerializer(serializers.ModelSerializer):
    class Meta: model = AwarenessSafety; exclude = ["visit", "created_at"]
class OcularExaminationSerializer(serializers.ModelSerializer):
    class Meta: model = OcularExamination; exclude = ["visit", "created_at"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["student_id", "name", "age", "gender", "school_name", "created_at"]

# --- Main Visit Serializer (With Safety Checks) ---
class ClinicalVisitSerializer(serializers.ModelSerializer):
    # Using 'get_...' properties avoids "RelatedObjectDoesNotExist" errors
    lifestyle = LifestyleBehaviorSerializer(source='get_lifestyle', read_only=True)
    environment = EnvironmentalFactorSerializer(source='get_environment', read_only=True)
    history = ClinicalHistorySerializer(source='get_clinical_history', read_only=True)
    awareness = AwarenessSafetySerializer(source='get_awareness', read_only=True)
    ocular = OcularExaminationSerializer(source='get_ocular_exam', read_only=True)

    class Meta:
        model = ClinicalVisit
        fields = ["id", "visit_date", "visit_type", "lifestyle", "environment", "history", "awareness", "ocular"]