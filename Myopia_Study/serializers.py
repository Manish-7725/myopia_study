from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Student,
    LifestyleBehavior,
    EnvironmentalFactor,
    ClinicalHistory,
    AwarenessSafety,
    ClinicalExamination,
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
        fields = "__all__"
        # read_only_fields = ["created_by", "created_at"]

class LifestyleBehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifestyleBehavior
        fields = [
            'outdoor_duration',
            'sun_exposure',
            'near_work_hours',
            'screen_time',
            'primary_device',
            'reading_distance',
            'viewing_posture_ratio',
            'dietary_habit',
            'dietary_other',
            'sleep_duration',
            'usual_bedtime',
        ]



class EnvironmentalFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalFactor
        fields = [
            "school_type",
            "classroom_strength",
            "seating_position",
            "teaching_methodology",
            "lighting",
            "sunlight_source",
        ]



class ClinicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalHistory
        fields = [
            "diagnosed_earlier",
            "age_at_diagnosis",
            "power_changed_last_3yrs",
            "compliance",
            "previous_re",
            "previous_le",
            "current_re",
            "current_le",
        ]



class AwarenessSafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessSafety
        fields = [
            "aware_eye_strain",
            "access_to_vision_care",   # ✅ added
            "follows_preventive_measures",
            "source_of_awareness",
        ]



class OcularExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcularExamination
        fields = [
            "ucva_re", "ucva_le",
            "bcva_re", "bcva_le",
            "cyclo_se_re", "cyclo_se_le",
            "spherical_re", "spherical_le",
            "axial_length_re", "axial_length_le",
            "keratometry_re", "keratometry_le",
            "cct_re", "cct_le",
            "anterior_segment_re", "anterior_segment_le",
            "amblyopia_or_strabismus",
            "fundus_re", "fundus_le",
        ]




class ClinicalExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalExamination
        exclude = ("student",)


class MyopiaVisitSubmissionSerializer(serializers.Serializer):
    student = StudentSerializer()
    lifestyle = LifestyleBehaviorSerializer()
    environment = EnvironmentalFactorSerializer()
    history = ClinicalHistorySerializer()
    awareness = AwarenessSafetySerializer()
    ocular = OcularExaminationSerializer()
    # examination = ClinicalExaminationSerializer()



from rest_framework import serializers
from .models import Student

class AdminStudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "name",
            "school_name",
            "age",
            "gender",
            "created_at",
        ]



from .models import (
    LifestyleBehavior,
    EnvironmentalFactor,
    ClinicalHistory,
    AwarenessSafety,
    OcularExamination
)

class LifestyleBehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifestyleBehavior
        exclude = ["student"]

class EnvironmentalFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalFactor
        exclude = ["student"]

class ClinicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalHistory
        exclude = ["student"]

class AwarenessSafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessSafety
        exclude = ["student"]

class OcularExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcularExamination
        exclude = ["student"]

class StudentProfileSerializer(serializers.ModelSerializer):
    lifestyles = LifestyleBehaviorSerializer(many=True, read_only=True)
    environments = EnvironmentalFactorSerializer(many=True, read_only=True)
    histories = ClinicalHistorySerializer(many=True, read_only=True)
    awareness = AwarenessSafetySerializer(many=True, read_only=True)
    ocular = OcularExaminationSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = "__all__"




class FollowUpSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.name")

    class Meta:
        model = ClinicalHistory
        fields = [
            "id",
            "student_name",
            "visit_date",
            "power_changed_last_3yrs",
            "compliance",
        ]



from django.contrib.auth import get_user_model
from .models import FollowUp
User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "date_joined"]

class FollowUpCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = '__all__'


class UserFormsListSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source="student.student_id")
    student_name = serializers.CharField(source="student.name")

    class Meta:
        model = ClinicalHistory
        fields = [
            "student_id",
            "student_name",
            "visit_date",
        ]
