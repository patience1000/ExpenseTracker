from .models import ExpenseCategory, Income, Expense, User
from rest_framework import serializers

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id','name']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    def get_category_name(self,obj):
        return obj.category.name
    
    source_income = serializers.SerializerMethodField()
    def get_source_income(self, obj):
        return obj.income_source.source
    class Meta:
        model = ExpenseCategory
        fields = ['id','date','amount','expense','description']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','source'] 

class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','date','amount','source']              


class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'url','username', 'email','password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

