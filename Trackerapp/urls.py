from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,IncomeViewSet, ExpenseViewSet, Login, Dashboard,AddExpense,get_user_expense, get_user_income

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'income',IncomeViewSet, basename='income')
router.register(r'expenses',ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', Login),
    path('', Dashboard),
    path('expense/', AddExpense),
    path('user-expenses/', get_user_expense),
    path('user-income/', get_user_income),
    
]
