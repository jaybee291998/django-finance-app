from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.
class BankAccount(models.Model):
	user 			= models.OneToOneField(User, related_name='bank_account', on_delete=models.CASCADE)
	balance			= models.IntegerField()

	def __str__(self):
		return f'{self.user.username} - Bank Account'

	def deposit(self, amount: int):
		"""
			add the specefied amount to the balance
		"""
		assert amount > 0
		assert isinstance(amount, int) or isinstance(amount, float)

		# add the amount to balance
		self.balance += amount
	
	def withdraw(self, amount: int):
		"""
			subtract the specified amount to the balance
		"""
		assert amount > 0 and amount <= self.balance

		# subtract the amount from the balance
		self.balance -= amount
	
	def get_balance(self):
		return f'current balance: {self.balance}'