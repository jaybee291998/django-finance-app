from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.DiaryListView.as_view(), name='diaries_list'),
    path('create/', views.DiaryCreateView.as_view(), name='diary_create'),
    path('detail/<int:pk>', views.DiaryDetailView.as_view(), name='diary_detail'),
    path('update/<int:pk>', views.DiaryUpdateView.as_view(), name='diary_update'),
    path('delete/<int:pk>', views.DiaryDeleteView.as_view(), name='diary_delete')
]
