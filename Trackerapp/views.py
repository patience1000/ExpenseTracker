from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category,Income,Expense
from .serializers import CategorySerializer, IncomeSerializer,ExpenseSerializer
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     self.queryset.filter(self.request.user)
class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     self.queryset.filter(self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer 
    permission_classes = [IsAuthenticated]  
 
    # def get_queryset(self):
    #     self.queryset.filter(self.request.user)     