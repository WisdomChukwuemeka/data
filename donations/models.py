from django.db import models
from django.utils import timezone
import uuid

class Donation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    donor_name = models.CharField(max_length=255)
    donor_email = models.EmailField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=100, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True)
    donated_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.donor_name} - {self.amount} ({self.status})"

    class Meta:
        ordering = ["-donated_at"]
