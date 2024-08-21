from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from Trackerapp.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import Category,Income,Expense,User
from django.views.decorators.csrf import csrf_exempt
from .serializers import CategorySerializer, IncomeSerializer,ExpenseSerializer
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def get_queryset(self):
        return  self.queryset.filter(user=self.request.user)

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def get_queryset(self):
        return  self.queryset.filter(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer 
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  
    def get_queryset(self):
        return  self.queryset.filter(user=self.request.user)
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_user_expense(request):
    user = request.user  # Get the authenticated user
    expenses = Expense.objects.filter(user=user) 
    data = []
    for expense in expenses:
        data.append({
            'category': expense.category.name,  
            'price': expense.price
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
