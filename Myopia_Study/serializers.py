from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Student,
    ClinicalVisit,

    OcularExamination,
   
)

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "name",
            "age",
            "gender",
            "school_name",
            "created_at",
        ]


# =====================================================
# Clinical Visit (timeline, admin)
# =====================================================
class ClinicalVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalVisit
        fields = [
            "id",
            "visit_date",
            "visit_type",
        ]


# =====================================================
# Ocular Examination (Section F)
# Used by baseline + follow-up
# =====================================================
class OcularExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcularExamination
        exclude = ["visit", "created_at"]


# =====================================================
# User Dashboard — computed serializer
# =====================================================
class UserStudentListSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    name = serializers.CharField()
    baseline_date = serializers.DateField(allow_null=True)
    last_visit_date = serializers.DateField(allow_null=True)
    can_create_baseline = serializers.BooleanField()
    can_create_followup = serializers.BooleanField()