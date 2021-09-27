from django.db import models

from bank_account.models import BankAccount
# Create your models here.


class FundType(models.Model):
	name 				= models.CharField(max_length=32)
	description			= models.TextField()

	def __str__(self):
		return self.name

class Fund(models.Model):
	account 			= models.ForeignKey(BankAccount, related_name='account_funds', on_delete=models.CASCADE, null=True)
	name 				= models.CharField(max_length=32)
	description 		= models.TextField()
	amount				= models.IntegerField()
	category			= models.ForeignKey(FundType, related_name='fund_category', on_delete=models.CASCADE, null=True)
	timestamp			= models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

