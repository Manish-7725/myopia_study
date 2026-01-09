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
        fields = ("username", "email", "password", "first_name", "last_name")
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "email", "full_name", "role", "date_joined", "last_login")

    def get_role(self, obj):
        return "Admin" if obj.is_staff else "User"

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

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
    follow_up_number = serializers.SerializerMethodField()
    last_visit = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["student_id", "name", "age", "gender", "school_name", "created_at", "status", "follow_up_number", "last_visit"]

    def get_follow_up_number(self, obj):
        return obj.clinicalvisit_set.filter(visit_type='FOLLOW_UP').count()

    def get_last_visit(self, obj):
        last_visit = obj.clinicalvisit_set.order_by('-visit_date').first()
        if last_visit:
            return last_visit.visit_date
        return None


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