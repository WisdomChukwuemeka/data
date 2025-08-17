from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ["id", "uuid", "donor_name", "donor_email", "amount", "payment_method", "transaction_id", "donated_at"]
        read_only_fields = ["id", "uuid", "payment_method", "transaction_id", "donated_at"]
