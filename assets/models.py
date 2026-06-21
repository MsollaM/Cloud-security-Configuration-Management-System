from django.db import models
from django.contrib.auth.models import User

class CloudAsset(models.Model):
    ASSET_TYPES = [
        ('server', 'Server'),
        ('database', 'Database'),
        ('storage', 'Storage'),
        ('network', 'Network Device'),
        ('application', 'Application'),
    ]
    STATUS_CHOICES = [
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('warning', 'Warning'),
        ('unknown', 'Unknown'),
    ]

    name = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    location = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    compliance_score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unknown')
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.asset_type})"

    def save(self, *args, **kwargs):
        if self.compliance_score < 60:
            self.status = 'non_compliant'
        elif self.compliance_score < 80:
            self.status = 'warning'
        elif self.compliance_score >= 80:
            self.status = 'compliant'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']