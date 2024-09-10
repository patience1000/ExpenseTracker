from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class Expense(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name

class ExpenseCategory(models.Model): 
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.ForeignKey(Expense, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    # income = models.ForeignKey(Income, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'ExpenseCategories'
    
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    source = models.TextField(max_length=100)
    
    def __str__(self):  
        return f'{self.source}'
    
class IncomeCategory(models.Model):
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    source = models.ForeignKey(Income, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=200)
    
    class Meta:
        verbose_name_plural = 'IncomeCategories'
    def __str__(self):  
        return f'{self.description}'    

class User(models.Model):
    username = models.TextField(max_length=100)
    email = models.EmailField()    