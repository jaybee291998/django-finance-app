from rest_framework import serializers
from .models import Fund, FundAllocationHistory

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'

class FundAllocationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FundAllocationHistory
        fields = ['description', 'fund', 'amount', 'is_allocate', 'timestamp']

class FundTransferHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FundTransferHistory
        fields = '__all__'