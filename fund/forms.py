from django import forms

class FundAllocationForm(forms.Form):
	ACTIONS = (
		('AL', 'Allocate'),
		('DL', 'Deallocate'))

	amount 			= forms.IntegerField()
	action 			= forms.ChoiceField(choices=ACTIONS)