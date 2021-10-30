from django import forms
from django.core.exceptions import ValidationError

class FundAllocationForm(forms.Form):
	ACTIONS = (
		('AL', 'Allocate'),
		('DL', 'Deallocate'))

	amount 			= forms.IntegerField()
	action 			= forms.ChoiceField(choices=ACTIONS)

	def clean_amount(self):
		amount = self.cleaned_data['amount']

		if amount < 0:
			raise ValidationError("Amount cant be negative")

		return amount