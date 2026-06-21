from django.db import models
from django.contrib.auth.models import User
from assets.models import CloudAsset

class Policy(models.Model):
    STANDARD_CHOICES = [
        ('iso27001', 'ISO 27001'),
        ('cis', 'CIS Benchmarks'),
        ('gdpr', 'GDPR'),
        ('custom', 'Custom'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    standard = models.CharField(max_length=50, choices=STANDARD_CHOICES, default='custom')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    applies_to = models.ManyToManyField(CloudAsset, blank=True, related_name='policies')
    version = models.CharField(max_length=20, default='1.0')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (v{self.version})"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Policies'