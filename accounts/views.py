from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import AuditLog, UserProfile
from .forms import UserProfileForm

@login_required
def admin_list(request):
    users = User.objects.all().select_related('profile')
    return render(request, 'accounts/admin_list.html', {'users': users})

@login_required
def audit_log_list(request):
    logs = AuditLog.objects.all()
    return render(request, 'accounts/audit_log.html', {'logs': logs})