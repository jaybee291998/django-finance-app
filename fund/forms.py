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

class FundTransferForm(forms.Form):
	def __init__(self, account, current_fund, *args, **kwargs):
		queryset = Fund.objects.filter(account=account).exclude(pk=current_fund.id)
		super(FundTransferForm, self).__init__(*args, **kwargs)
		self.fields['recipient_fund'].queryset = queryset

	recipient_fund 		= forms.ModelChoiceField(queryset=None, initial=0)
	amount 				= forms.IntegerField()

	def clean_amount(self):
		amount = self.cleaned_data.get('amount')

		if amount > current_fund.amount:
			raise ValidationError(f'You have insufficient amount to transfer.\nCurrent balance:{current_fund.amount}')

		return amount