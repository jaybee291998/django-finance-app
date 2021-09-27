# Generated by Django 3.2.7 on 2021-09-26 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0011_remove_fund_account'),
        ('fund', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='fund',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fund_expenses', to='fund.fund'),
        ),
        migrations.DeleteModel(
            name='Fund',
        ),
    ]
