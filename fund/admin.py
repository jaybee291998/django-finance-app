from django.contrib import admin
from .models import FundType, Fund, FundTransferHistory, FundAllocationHistory
# Register your models here.

admin.site.register(Fund)
admin.site.register(FundType)
admin.site.register(FundTransferHistory)
admin.site.register(FundAllocationHistory)
