from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assets.models import CloudAsset
from reports.models import ComplianceReport

@login_required
def dashboard(request):
    total_assets = CloudAsset.objects.count()
    compliant = CloudAsset.objects.filter(status='compliant').count()
    non_compliant = CloudAsset.objects.filter(status='non_compliant').count()
    warning = CloudAsset.objects.filter(status='warning').count()
    total_reports = ComplianceReport.objects.count()
    recent_assets = CloudAsset.objects.order_by('-created_at')[:5]
    context = {
        'total_assets': total_assets,
        'compliant': compliant,
        'non_compliant': non_compliant,
        'warning': warning,
        'total_reports': total_reports,
        'recent_assets': recent_assets,
    }
    return render(request, 'dashboard.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('assets/', include('assets.urls')),
    path('policies/', include('policies.urls')),
    path('reports/', include('reports.urls')),
    path('accounts/', include('accounts.urls')),
]