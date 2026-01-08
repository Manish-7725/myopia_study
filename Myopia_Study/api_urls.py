from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_auth, api_forms, api_students, api_admin

router = DefaultRouter()
router.register(r'admin/users', api_admin.UserViewSet, basename='user')

urlpatterns = [
    # Auth
    path('signup/', api_auth.signup_api, name='api-signup'),
    path('login/', api_auth.login_api, name='api-login'),
    path("user/profile/", api_auth.user_profile, name='user-profile'),

    # User Dashboard
    path("user/overview/", api_forms.user_dashboard_overview, name='user-overview'),
    path("user/students/", api_students.user_students, name='user-students'),
    path("user/student/<str:student_id>/visits/", api_students.user_student_visits, name='user-student-visits'),
    path("user/forms/", api_students.user_forms, name='user-forms'),
    path("user/recent-activity/", api_students.user_recent_activity, name='user-recent-activity'),
    path("user/followups/", api_students.user_followups, name='user-followups'),

    # Forms
    path("forms/submit-student/", api_forms.submit_student_form, name='submit-student'),
    path("forms/submit-followup/", api_forms.submit_followup_form, name='submit-followup'),

    # Admin Dashboard
    path("", include(router.urls)),
    path("admin/overview/", api_admin.admin_overview),
    path("admin/students/", api_admin.admin_students_list),
    path("admin/student/<str:student_id>/", api_admin.admin_student_detail),
    path("admin/user/<int:user_id>/reset-password/", api_admin.admin_reset_password, name='admin-reset-password'),
    path("admin/user/<int:user_id>/force-logout/", api_admin.admin_force_logout, name='admin-force-logout'),
    
    # Export
    path("admin/export/excel/", api_admin.ExportClinicalDataView.as_view(), name='export-excel'),
]