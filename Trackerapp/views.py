from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from Trackerapp.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import ExpenseCategory,Income,Expense,User
from django.views.decorators.csrf import csrf_exempt
from .serializers import IncomeCategorySerializer, IncomeSerializer,ExpenseSerializer, UserSerializers
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

# Create your views here.
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def get_queryset(self):
        return  self.queryset.filter(user=self.request.user)
    
class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer 
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  
    def get_queryset(self):
        return  self.queryset.filter(user=self.request.user)
    
class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def get_queryset(self):
        return  self.queryset.filter(user=self.request.user)
    
class IncomeCategoryViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeCategorySerializer
    permission_classes = [IsAuthenticated]

@api_view('GET')
@permission_classes([IsAuthenticated])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializers(users, many=True)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_expense(request):
    user = request.user  # Get the authenticated user
    expenses = ExpenseCategory.objects.filter(user=user) 
    data = []
    for expense in expenses:
        data.append({
            'expense_type': expense.expense_type.name,  
            'amount': expense.amount
        })
    
    return JsonResponse(data,safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_income(request):
    user = request.user
    income = Income.objects.filter(user=user)
    data = []
    for i in income:
        data.append({
            'source': i.source,
            'amount': i.amount
        })
    return JsonResponse(data,safe=False)  
    
@csrf_exempt  
def Login(request):
    return render(request, 'Trackerapp/login.html')
def Dashboard(request):
    return render(request, 'Trackerapp/index.html')
def AddExpense(request):
    return render(request, 'Trackerapp/expense.html')

@permission_classes([IsAuthenticated])
def CategoryView(request):
    pat = User.objects.get(pk=1)
    if pat.groups.filter(name='editor').exists():
        def get_queryset(self):
          return  self.queryset.filter(user=self.request.user)