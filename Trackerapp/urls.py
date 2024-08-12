from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,IncomeViewSet, ExpenseViewSet, UserViewSet, LoginViewSet, Login1,Dashboard

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'income',IncomeViewSet, basename='income')
router.register(r'expenses',ExpenseViewSet, basename='expenses')
router.register(r'users', UserViewSet)
router.register(r'login',LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
    path('login1/', Login1),
    path('dashboard/', Dashboard),
]
