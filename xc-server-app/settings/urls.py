from django.urls import path
from .views import ProfileView, BudgetListCreateView, BudgetRetrieveUpdateDestroyView, AccountDeleteView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('budget/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('budget/<int:pk>/', BudgetRetrieveUpdateDestroyView.as_view(), name='budget-detail'),
    path('account/delete/', AccountDeleteView.as_view(), name='account-delete'),
]