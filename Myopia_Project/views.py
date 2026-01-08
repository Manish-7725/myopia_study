from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard_view(request):
    return render(request, 'admin_dash.html')