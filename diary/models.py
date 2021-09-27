from django.db import models
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()
# Create your models here.
class Diary(models.Model):
	title 				= models.CharField(max_length=32)
	content 			= models.TextField()
	timestamp			= models.DateTimeField(auto_now_add=True)
	user 				= models.ForeignKey(User, related_name='user_diary', on_delete=models.CASCADE, null=True)

	def __str__(self):
		return f'{self.title} - {self.content[:15]}'

