# api_urls.py
from django.urls import path

from Myopia_Study import api_admin
from . import api_followups
from . import api_auth
from . import api_forms
from .api_students import students_api
from .api_forms import submit_myopia_form, UserFormsList


urlpatterns = [
    path('signup/', api_auth.signup_api, name='api-signup'),
    path('login/', api_auth.login_api, name='api-login'),
    path("students/", students_api),
    path("forms/submit/", submit_myopia_form),
    path("followups/", api_followups.list_followups),
    path("followups/create/", api_followups.create_followup),

    # Admin APIs
    path("admin/overview/", api_admin.admin_overview),
    path("admin/students/", api_admin.admin_students),
    path("admin/student/<str:student_id>/", api_admin.admin_student_detail),
    path("admin/student/<str:student_id>/visit/<str:visit_date>/", api_admin.admin_edit_visit),
    # path("admin/export/students/csv/", api_admin.export_students),
    # path("admin/export/students/excel/", api_admin.export_students_excel),
    # path("admin/students-export/", api_admin.students_export_json),
    path("followups/", api_followups.list_followups),
    path("followups/create/", api_followups.create_followup),

    path("admin/users/", api_admin.admin_users),
    path("admin/users/create/", api_admin.admin_create_user),
    path("admin/activity-analytics/", api_admin.activity_analytics),

    #user's path 
    path("user/overview/", api_forms.user_dashboard_overview),
    path("user/profile/", api_auth.user_profile),
    path("user/forms/", UserFormsList.as_view()),
    path("user/students/", api_students.user_students),

        ]