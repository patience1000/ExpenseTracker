from .models import Category, Income, Expense, User
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
    
    source_income = serializers.SerializerMethodField()
    def get_source_income(self, obj):
        return obj.income_source.source
    class Meta:
        model = Expense
        fields = ['id','date','price','category','category_name','description','income_source','source_income']

class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url','username', 'email','password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
