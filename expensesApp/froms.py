from django.forms import ModelForm
from .models import Category, Expense
from django import forms


class categoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['user']


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ('amount',)


# ── User Story 1: Set Initial Budget Cycle ──────────────────────────────────
class CycleForm(forms.Form):
    total_allowance = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Total Cash Allowance ($)",
    )
    duration_days = forms.IntegerField(
        min_value=1,
        max_value=365,
        label="Cycle Duration (days)",
    )
