from rest_framework import serializers
from .models import FundAllocationHistory

class FundAllocationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FundAllocationHistory
        fields = ['fund', 'amount', 'is_allocate', 'timestamp']