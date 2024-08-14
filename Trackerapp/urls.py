from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,IncomeViewSet, ExpenseViewSet, Login1,Dashboard, Success,get_user_expense

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'income',IncomeViewSet, basename='income')
router.register(r'expenses',ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('api', include(router.urls)),
    path('login1/', Login1),
    path('', Dashboard),
    path('user-expenses/', get_user_expense),
    path('',Success),
]
