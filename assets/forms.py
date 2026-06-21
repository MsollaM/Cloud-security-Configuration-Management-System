from django import forms
from .models import CloudAsset

class CloudAssetForm(forms.ModelForm):
    class Meta:
        model = CloudAsset
        fields = ['name', 'asset_type', 'ip_address', 'location', 'owner',
                  'compliance_score', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'asset_type': forms.Select(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control'}),
            'compliance_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }