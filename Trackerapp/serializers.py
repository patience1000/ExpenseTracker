from .models import Category, Income, Expense
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','date','amount','source']       

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    def get_category_name(self,obj):
        return obj.category.name
    
    income_source = serializers.SerializerMethodField()
    def get_income_source(self, obj):
        return obj.income_source.source
    class Meta:
        model = Expense
        fields = ['id','date','price','category_name','description','income_source']