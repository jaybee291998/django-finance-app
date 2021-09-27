from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.FundListView.as_view(), name='funds_list'),
    path('create/', views.FundCreateView.as_view(), name='fund_create'),
    path('detail/<int:pk>', views.FundDetailView.as_view(), name='fund_detail'),
    path('update/<int:pk>', views.FundUpdateView.as_view(), name='fund_update'),
    path('delete/<int:pk>', views.FundDeleteView.as_view(), name='fund_delete')
]
