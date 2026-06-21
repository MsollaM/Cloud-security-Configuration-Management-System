from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CloudAsset
from .forms import CloudAssetForm
from accounts.models import AuditLog

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

@login_required
def asset_list(request):
    query = request.GET.get('q', '')
    assets = CloudAsset.objects.all()
    if query:
        assets = assets.filter(name__icontains=query)
    return render(request, 'assets/asset_list.html', {'assets': assets, 'query': query})

@login_required
def asset_create(request):
    form = CloudAssetForm(request.POST or None)
    if form.is_valid():
        asset = form.save(commit=False)
        asset.created_by = request.user
        asset.save()
        AuditLog.objects.create(
            user=request.user, action='create', model_name='CloudAsset',
            object_id=str(asset.id), description=f'Created asset: {asset.name}',
            ip_address=get_client_ip(request)
        )
        messages.success(request, f'Asset "{asset.name}" created successfully.')
        return redirect('asset_list')
    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Add New Asset'})

@login_required
def asset_update(request, pk):
    asset = get_object_or_404(CloudAsset, pk=pk)
    form = CloudAssetForm(request.POST or None, instance=asset)
    if form.is_valid():
        form.save()
        AuditLog.objects.create(
            user=request.user, action='update', model_name='CloudAsset',
            object_id=str(asset.id), description=f'Updated asset: {asset.name}',
            ip_address=get_client_ip(request)
        )
        messages.success(request, f'Asset "{asset.name}" updated successfully.')
        return redirect('asset_list')
    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Edit Asset'})

@login_required
def asset_delete(request, pk):
    asset = get_object_or_404(CloudAsset, pk=pk)
    if request.method == 'POST':
        name = asset.name
        AuditLog.objects.create(
            user=request.user, action='delete', model_name='CloudAsset',
            object_id=str(asset.id), description=f'Deleted asset: {name}',
            ip_address=get_client_ip(request)
        )
        asset.delete()
        messages.success(request, f'Asset "{name}" deleted.')
        return redirect('asset_list')
    return render(request, 'assets/asset_confirm_delete.html', {'asset': asset})