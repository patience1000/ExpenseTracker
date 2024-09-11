from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncomeCategoryViewSet, ExpenseCategoryViewSet,ExpenseViewSet, UserViewSet, Login, Dashboard,AddExpense,get_user_expense,AddIncome, CurrentUserView

router = DefaultRouter()
router.register(r'categories', ExpenseViewSet, basename='category')
router.register(r'income',IncomeCategoryViewSet, basename='income')
router.register(r'users',UserViewSet, basename='user')
# router.register(r'expenses',ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', Login),
    path('', Dashboard),
    path('expense/', AddExpense),
    path('income/', AddIncome),
    path('user-expenses/', get_user_expense),
    path('me/', CurrentUserView.as_view(), name='current-user')
]
