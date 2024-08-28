from django.contrib import admin
from .models import Income, IncomeCategory, Expense,ExpenseCategory
# Register your models here.
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(ExpenseCategory)
admin.site.register(IncomeCategory)
