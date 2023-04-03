from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('seznam/', views.seznamListView.as_view(), name='seznam'),
    path('seznam/<int:pk>', views.seznamDetailView.as_view(), name='seznam_detail'),
]
