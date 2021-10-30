from django import forms 
from .models import Income
from django.core.exceptions import ValidationError  

class IncomeAddForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		self.prev_instance = kwargs.pop('prev_instance')
		super(IncomeAddForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Income
		fields = [
			'description',
			'category',
			'amount',
			'source'
		]

	def clean_amount(self):
		amount = self.cleaned_data['amount']
		# only accept positive integers
		if amount < 0:
			raise ValidationError('Negative Integers are not allowed')

		if self.prev_instance is not None:
			prev_amount = self.prev_instance.amount
			bank_account = self.request.user.bank_account
			# if the prev_amount is reduced
			if amount < prev_amount:
				# if the amount reduced is greater than  the unallocated balance
				if (prev_amount - amount) > bank_account.balance:
					raise ValidationError(f'You cannot reduce this income by {prev_amount - amount}, because it is already in use')
		
		return amount
