from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from Trackerapp.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import Category,Income,Expense,User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import CategorySerializer, IncomeSerializer,ExpenseSerializer,UserSerializers
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
    
    # added this function so I can get each user and their expenses so that I can use it in the chart 
    def get_user(request):
        user_id = User
        expenses = Expense.objects.filter(user_id=user_id)
        data = []
        for expense in expenses:
            data.append({
                'category': expense.category,
                'price': expense.price
            })
        return JsonResponse(data, safe=False)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers        

class LoginViewSet(viewsets.ViewSet):
    def create(self,request):
        serializer = ObtainAuthToken.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token  = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        })

#added this block for template login    
@csrf_exempt  
def Login1(request):
    return render(request, 'Trackerapp/login.html')
def Dashboard(request):
    return render(request, 'Trackerapp/index.html')