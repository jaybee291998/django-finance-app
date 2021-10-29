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
		
		return amount
