from django import forms
from .models import ComplianceReport

class ComplianceReportForm(forms.ModelForm):
    class Meta:
        model = ComplianceReport
        fields = ['title', 'asset', 'policy', 'status', 'findings', 'recommendations', 'score']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'asset': forms.Select(attrs={'class': 'form-control'}),
            'policy': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'findings': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }