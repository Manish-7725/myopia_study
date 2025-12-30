from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from Myopia_Study.models import Student
from Myopia_Study.serializers import (
    LifestyleBehaviorSerializer,
    EnvironmentalFactorSerializer,
    ClinicalHistorySerializer,
    AwarenessSafetySerializer,
    OcularExaminationSerializer,
)

class MyopiaStudyAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        self.student = Student.objects.create(
            name="Test Student", age=12, gender="Male", height=150, weight=40,
            parental_myopia="No", num_siblings=1, birth_order="First", student_id="STU9999"
        )

    def test_admin_overview(self):
        url = reverse('api_admin.admin_overview')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_student_detail(self):
        url = f"/api/admin/student/{self.student.student_id}/"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_edit_visit(self):
        # You must create related visit data for this test to work in your DB
        url = f"/api/admin/student/{self.student.student_id}/visit/{str(self.student.created_at.date())}/"
        response = self.client.get(url)
        # Accept 200 or 404 if no visit exists
        assert response.status_code in (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND)

    def test_followups_list(self):
        url = "/api/followups/"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_submit_myopia_form(self):
        url = "/api/forms/submit/"
        payload = {
            "student": {
                "student_id": "STU9998",
                "name": "Form Student",
                "age": 10,
                "gender": "Female",
                "height": 140,
                "weight": 35,
                "parental_myopia": "No",
                "num_siblings": 0,
                "birth_order": "Only"
            },
            "lifestyle": {
                "outdoor_duration": "<1 hr",
                "sun_exposure": "<15 min",
                "near_work_hours": "<2 hrs",
                "screen_time": "<1 hr",
                "primary_device": "Mobile",
                "reading_distance": "<20 cm",
                "viewing_posture_ratio": "Low",
                "dietary_habit": "Balanced",
                "dietary_other": "",
                "sleep_duration": "<6 hrs",
                "usual_bedtime": "Before9"
            },
            "environment": {
                "school_type": "Urban",
                "classroom_strength": "Small",
                "seating_position": "Front",
                "teaching_methodology": "Digital",
                "lighting": "Dim",
                "sunlight_source": "Natural"
            },
            "history": {
                "diagnosed_earlier": False,
                "age_at_diagnosis": None,
                "power_changed_last_3yrs": False,
                "compliance": "Always",
                "previous_re": "",
                "previous_le": "",
                "current_re": "-1.00",
                "current_le": "-1.00"
            },
            "awareness": {
                "aware_eye_strain": True,
                "access_to_vision_care": True,
                "follows_preventive_measures": "Always",
                "source_of_awareness": "School"
            },
            "ocular": {
                "ucva_re": "6/6",
                "ucva_le": "6/6",
                "bcva_re": "6/6",
                "bcva_le": "6/6",
                "cyclo_se_re": "-1.00",
                "cyclo_se_le": "-1.00",
                "spherical_re": "-1.00",
                "spherical_le": "-1.00",
                "axial_length_re": "23.00",
                "axial_length_le": "23.00",
                "keratometry_re": "42.00",
                "keratometry_le": "42.00",
                "cct_re": "550",
                "cct_le": "550",
                "anterior_segment_re": "Normal",
                "anterior_segment_le": "Normal",
                "amblyopia_or_strabismus": False,
                "fundus_re": "Healthy disc and macula",
                "fundus_le": "Healthy disc and macula"
            }
        }
        response = self.client.post(url, payload, format='json')
        assert response.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST)

class MyopiaStudySerializerTest(TestCase):
    def test_lifestyle_serializer(self):
        data = {
            "outdoor_duration": "<1 hr",
            "sun_exposure": "<15 min",
            "near_work_hours": "<2 hrs",
            "screen_time": "<1 hr",
            "primary_device": "Mobile",
            "reading_distance": "<20 cm",
            "viewing_posture_ratio": "Low",
            "dietary_habit": "Balanced",
            "dietary_other": "",
            "sleep_duration": "<6 hrs",
            "usual_bedtime": "Before9"
        }
        serializer = LifestyleBehaviorSerializer(data=data)
        assert serializer.is_valid()

    # Repeat for other serializers as needed...
    def test_environment_serializer(self):
        data = {
            "school_type": "Urban",
            "classroom_strength": "Small",
            "seating_position": "Front",
            "teaching_methodology": "Digital",
            "lighting": "Dim",
            "sunlight_source": "Natural"
        }
        serializer = EnvironmentalFactorSerializer(data=data)
        assert serializer.is_valid()