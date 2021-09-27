from django.db import models

from bank_account.models import BankAccount
# Create your models here.


class IncomeType(models.Model):
	name 				= models.CharField(max_length=32)
	description			= models.TextField()

	def __str__(self):
		return self.name

class Income(models.Model):
	description 		= models.TextField()
	category 			= models.ForeignKey(IncomeType, related_name='income', on_delete=models.CASCADE, null=True)
	amount				= models.IntegerField(default=0)
	source				= models.CharField(max_length=32, null=True)
	timestamp			= models.DateTimeField(auto_now_add=True)
	account 			= models.ForeignKey(BankAccount, related_name='user_income', on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.description[:10] + ' - ' + str(self.category)

