from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.FundListView.as_view(), name='funds_list'),
    path('create/', views.FundCreateView.as_view(), name='fund_create'),
    path('detail/<int:pk>', views.FundDetailView.as_view(), name='fund_detail'),
    path('update/<int:pk>', views.FundUpdateView.as_view(), name='fund_update'),
    path('delete/<int:pk>', views.FundDeleteView.as_view(), name='fund_delete'),
    path('fund_allocation/<int:fund_id>', views.fund_allocation_view, name='fund_allocation'),
    path('fund_transfer/<int:fund_id>', views.transfer_FTF, name='fund_transfer'),
    path('fund_allocation_history_list_api/', views.FundAllocationHistoryList.as_view(), name='fund_allocation_history_list_api'),
    path('fund_allocation_history_list/', views.fund_allocation_list_view, name='fund_allocation_history_list'),
    path('api/fund_list/', views.FundList.as_view(), name="fund_list_api")
]
