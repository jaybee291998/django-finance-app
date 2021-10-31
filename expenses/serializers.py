from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.Serializer):

	CATEGORY_CHOICES = [('FD', 'FOOD'), ('SK', 'SNACKS'), ('CL', 'CLOTHING'), ('OS', 'ONLINE_SHOPPING')]

	id 				= serializers.IntegerField(read_only=True)
	description 	= serializers.CharField()
	category	 	= serializers.ChoiceField(choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][1])
	price 			= serializers.IntegerField(default=0)
	timestamp 		= serializers.DateTimeField()

	def create(self, validated_data):
		
		return Expense.objects.create(**validated_data)

	def update(self, instance, validated_data):

		instance.description 	= validated_data.get('description', instance.description)
		instance.category 		= validated_data.get('category', instance.category)
		instance.price 			= validated_data.get('price', instance.price)
		instance.save()
		return instance

class ExpenseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Expense
		fields = ['id', 'description', 'category', 'price', 'timestamp']

