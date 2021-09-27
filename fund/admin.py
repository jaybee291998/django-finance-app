from django.contrib import admin
from .models import FundType, Fund
# Register your models here.

admin.site.register(Fund)
admin.site.register(FundType)
