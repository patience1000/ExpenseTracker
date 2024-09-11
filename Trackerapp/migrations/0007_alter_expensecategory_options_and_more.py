# Generated by Django 5.1 on 2024-09-11 13:44

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trackerapp', '0006_user_remove_expense_category_remove_expense_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expensecategory',
            options={'verbose_name_plural': 'ExpenseCategories'},
        ),
        migrations.AlterModelOptions(
            name='incomecategory',
            options={'verbose_name_plural': 'IncomeCategories'},
        ),
        migrations.RenameField(
            model_name='expensecategory',
            old_name='expense_type',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='income',
            old_name='source',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='expensecategory',
            name='description',
        ),
        migrations.AddField(
            model_name='expensecategory',
            name='category_description',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='expensecategory',
            name='income',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Trackerapp.incomecategory'),
        ),
        migrations.AddField(
            model_name='incomecategory',
            name='income_description',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='expensecategory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='incomecategory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
