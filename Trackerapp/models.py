from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    name = models.TextField(max_length=100)   

class IncomeCategory(models.Model):
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    source = models.ForeignKey(Income, on_delete=models.CASCADE, null=True)
    income_description = models.TextField(max_length=200, null=True)
    
    class Meta:
        verbose_name_plural = 'IncomeCategories'
    def __str__(self):  
        return f'{self.income_description}'
    
class Expense(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
         
class ExpenseCategory(models.Model): 
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Expense, on_delete=models.CASCADE)
    category_description = models.TextField(max_length=200, null=True)
    income = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name_plural = 'ExpenseCategories'
    
    def __str__(self):  
        return f'{self.category_description}'   

class User(models.Model):
    username = models.TextField(max_length=100)
    email = models.EmailField()    