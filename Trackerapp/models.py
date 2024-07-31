from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class Income(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    source = models.TextField(max_length=200)
    
    def __str__(self):  
        return f'{self.source}'
    
class Expense(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    income_source = models.ForeignKey(Income, on_delete=models.CASCADE)
     
    def __str__(self):
        return f'{self.category.name} - {self.description}'