from django.urls import path
from .views import addExpense, addCategory, displayAllexpenses, setCycle, spendingInsights

urlpatterns = [
    # ── Existing ──────────────────────────────────────────────────────────────
    path('addExpense/',      addExpense,         name='addExpense'),
    path('addcategory/',     addCategory,        name='addCategory'),
    path('showAllexpenses/', displayAllexpenses, name='dislpayExpenses'),

    # ── User Story 1: Set Initial Budget Cycle ────────────────────────────────
    path('setCycle/',        setCycle,           name='setCycle'),

    # ── User Story 3: Visual Spending Insights ────────────────────────────────
    path('insights/',        spendingInsights,   name='spendingInsights'),
]
