from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Policy
from .forms import PolicyForm
from accounts.models import AuditLog

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

@login_required
def policy_list(request):
    query = request.GET.get('q', '')
    policies = Policy.objects.all()
    if query:
        policies = policies.filter(name__icontains=query)
    return render(request, 'policies/policy_list.html', {'policies': policies, 'query': query})

@login_required
def policy_create(request):
    form = PolicyForm(request.POST or None)
    if form.is_valid():
        policy = form.save(commit=False)
        policy.created_by = request.user
        policy.save()
        form.save_m2m()
        AuditLog.objects.create(
            user=request.user, action='create', model_name='Policy',
            object_id=str(policy.id), description=f'Created policy: {policy.name}',
            ip_address=get_client_ip(request)
        )
        messages.success(request, f'Policy "{policy.name}" created successfully.')
        return redirect('policy_list')
    return render(request, 'policies/policy_form.html', {'form': form, 'title': 'Add New Policy'})

@login_required
def policy_update(request, pk):
    policy = get_object_or_404(Policy, pk=pk)
    form = PolicyForm(request.POST or None, instance=policy)
    if form.is_valid():
        form.save()
        AuditLog.objects.create(
            user=request.user, action='update', model_name='Policy',
            object_id=str(policy.id), description=f'Updated policy: {policy.name}',
            ip_address=get_client_ip(request)
        )
        messages.success(request, f'Policy "{policy.name}" updated.')
        return redirect('policy_list')
    return render(request, 'policies/policy_form.html', {'form': form, 'title': 'Edit Policy'})

@login_required
def policy_delete(request, pk):
    policy = get_object_or_404(Policy, pk=pk)
    if request.method == 'POST':
        name = policy.name
        AuditLog.objects.create(
            user=request.user, action='delete', model_name='Policy',
            object_id=str(policy.id), description=f'Deleted policy: {name}',
            ip_address=get_client_ip(request)
        )
        policy.delete()
        messages.success(request, f'Policy "{name}" deleted.')
        return redirect('policy_list')
    return render(request, 'policies/policy_confirm_delete.html', {'policy': policy})