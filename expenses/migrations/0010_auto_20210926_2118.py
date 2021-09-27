# Generated by Django 3.2.7 on 2021-09-26 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0001_initial'),
        ('expenses', '0009_auto_20210926_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='user',
        ),
        migrations.RemoveField(
            model_name='fund',
            name='user',
        ),
        migrations.AddField(
            model_name='expense',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_expenses', to='bank_account.bankaccount'),
        ),
        migrations.AddField(
            model_name='fund',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_funds', to='bank_account.bankaccount'),
        ),
    ]
