from django.urls import path
from .views import addExpense, addCategory, displayAllexpenses, setCycle, spendingInsights,edit_category,delete_category,category_list

urlpatterns = [
    # ── Existing ──────────────────────────────────────────────────────────────
    path('addExpense/',      addExpense,         name='addExpense'),
    path('addcategory/',     addCategory,        name='addCategory'),
    path('showAllexpenses/', displayAllexpenses, name='dislpayExpenses'),
    path('categories/', category_list, name='category_list'),
    path('categories/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
    
    # ── User Story 1: Set Initial Budget Cycle ────────────────────────────────
    path('setCycle/',        setCycle,           name='setCycle'),

    # ── User Story 3: Visual Spending Insights ────────────────────────────────
    path('insights/',        spendingInsights,   name='spendingInsights'),
]
