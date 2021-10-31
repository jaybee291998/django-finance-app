from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Expense
		fields = ['description', 'category', 'price', 'timestamp', 'fund', 'account']

class ExpenseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Expense
		fields = ['id', 'description', 'category', 'price', 'fund', 'timestamp']

