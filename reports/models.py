from django.db import models
from django.contrib.auth.models import User
from assets.models import CloudAsset
from policies.models import Policy

class ComplianceReport(models.Model):
    STATUS_CHOICES = [
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('warning', 'Warning'),
    ]

    title = models.CharField(max_length=200)
    asset = models.ForeignKey(CloudAsset, on_delete=models.CASCADE, related_name='reports')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='reports')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    findings = models.TextField()
    recommendations = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.status.upper()}"

    class Meta:
        ordering = ['-generated_at']