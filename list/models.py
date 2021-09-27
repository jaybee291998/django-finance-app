from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class List(models.Model):
	title 				= models.CharField(max_length=32)
	description 		= models.TextField()
	timestamp			= models.DateTimeField(auto_now_add=True)
	user 				= models.ForeignKey(User, related_name='list', on_delete=models.CASCADE, null=True)

	def __str__(self):
		return f'{self.title} - {self.description[:15]}'

class ListEntry(models.Model):
	list_obj			= models.ForeignKey(List, related_name='list_entries', on_delete=models.CASCADE, null=True)
	content 			= models.TextField()
	timestamp 			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.list_obj.title} - {self.content[:10]}'