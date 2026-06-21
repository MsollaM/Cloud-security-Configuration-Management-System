from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ComplianceReport
from .forms import ComplianceReportForm
from accounts.models import AuditLog

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

@login_required
def report_list(request):
    query = request.GET.get('q', '')
    reports = ComplianceReport.objects.all()
    if query:
        reports = reports.filter(title__icontains=query)
    return render(request, 'reports/report_list.html', {'reports': reports, 'query': query})

@login_required
def report_create(request):
    form = ComplianceReportForm(request.POST or None)
    if form.is_valid():
        report = form.save(commit=False)
        report.generated_by = request.user
        report.save()
        AuditLog.objects.create(
            user=request.user, action='create', model_name='ComplianceReport',
            object_id=str(report.id), description=f'Generated report: {report.title}',
            ip_address=get_client_ip(request)
        )
        messages.success(request, f'Report "{report.title}" generated successfully.')
        return redirect('report_list')
    return render(request, 'reports/report_form.html', {'form': form, 'title': 'Generate Report'})

@login_required
def report_delete(request, pk):
    report = get_object_or_404(ComplianceReport, pk=pk)
    if request.method == 'POST':
        title = report.title
        AuditLog.objects.create(
            user=request.user, action='delete', model_name='ComplianceReport',
            object_id=str(report.id), description=f'Deleted report: {title}',
            ip_address=get_client_ip(request)
        )
        report.delete()
        messages.success(request, f'Report "{title}" deleted.')
        return redirect('report_list')
    return render(request, 'reports/report_confirm_delete.html', {'report': report})