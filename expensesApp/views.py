from django.shortcuts import render, redirect
from .froms import ExpenseForm, categoryForm, CycleForm
from .models import Category, Cycle, Expense
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.db.models import Sum


@login_required(login_url='login')
def addExpense(request):
    form = ExpenseForm()
    allcategories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = ExpenseForm(request.POST)
            category = request.POST.get("categories")
            if form.is_valid():
                exp = form.save(commit=False)
                exp.user = request.user

                try:
                    categ = Category.objects.get(name=category, user=request.user)
                    exp.category = categ
                except:
                    messages.error(request, 'such category doesnot exist add it to complete the process')
                    return render(request, 'expenssesApp/addExpense.html', {'form': form, 'categories': allcategories})

                try:
                    currentCycle = Cycle.objects.get(user=request.user)
                    if currentCycle.is_active:
                        exp.cycle = currentCycle
                        exp.save()
                        messages.success(request, 'expense added successfully!')

                        # ─── إضافة التحذير بعد الحفظ ─────────────────
                        today = timezone.now().date()
                        today_spent = Expense.objects.filter(
                            user=request.user,
                            cycle=currentCycle,
                            time_stamp__date=today
                        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

                        remaining = currentCycle.total_allowance - (
                            Expense.objects.filter(user=request.user, cycle=currentCycle)
                            .aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
                        )
                        days_rem = max((currentCycle.end_date - today).days + 1, 1)
                        safe_limit = remaining / Decimal(days_rem)

                        if today_spent > safe_limit:
                            messages.warning(
                                request,
                                f'⚠️ You exceed the daily safe limit! You have spent ${today_spent:.2f} '
                                f'while your safe limit is ${safe_limit:.2f}'
                            )
                    else:
                        messages.error(request, "cycle is not active")
                except:
                    messages.error(request, 'there is no cycle add cycle first')

    return render(request, 'expenssesApp/addExpense.html', {'form': form, 'categories': allcategories})


# ── Existing: Add Category ───────────────────────────────────────────────────
@login_required(login_url='login')
def addCategory(request):
    form = categoryForm()
    if request.method == "POST":
        if request.user.is_authenticated:
            form = categoryForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    obj = form.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    messages.success(request, 'category added successfully!')
                except:
                    messages.error(request, 'category already exist')
    return render(request, 'expenssesApp/addCategory.html', {'form': form})


# ── Existing: Display All Expenses ───────────────────────────────────────────
@login_required(login_url='login')
def displayAllexpenses(request):
    allExpenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenssesApp/Expenses.html', {'expenses': allExpenses})


# ── User Story 1: Set Initial Budget Cycle ───────────────────────────────────
@login_required(login_url='login')
def setCycle(request):
    """
    The student inputs their total cash allowance and the number of days in
    their spending cycle.  The system computes start_date, end_date, and the
    starting daily limit, then saves (or updates) the Cycle for this user.
    """
    existing_cycle = Cycle.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = CycleForm(request.POST)
        if form.is_valid():
            total_allowance = form.cleaned_data['total_allowance']
            duration_days   = form.cleaned_data['duration_days']

            start_date = timezone.now().date()
            end_date   = start_date + timedelta(days=duration_days - 1)

            if existing_cycle:
                existing_cycle.total_allowance = total_allowance
                existing_cycle.start_date      = start_date
                existing_cycle.end_date        = end_date
                existing_cycle.is_active       = True
                existing_cycle.save()
                messages.success(request, "Budget cycle updated successfully!")
            else:
                Cycle.objects.create(
                    user=request.user,
                    total_allowance=total_allowance,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True,
                )
                messages.success(request, "Budget cycle created successfully!")

            return redirect('home')
    else:
        # Pre-fill the form if a cycle already exists
        initial = {}
        if existing_cycle:
            days = (existing_cycle.end_date - existing_cycle.start_date).days + 1
            initial = {
                'total_allowance': existing_cycle.total_allowance,
                'duration_days':   days,
            }
        form = CycleForm(initial=initial)

    # Compute current daily limit to show on the page (server-side only)
    preview_daily_limit = None
    if existing_cycle:
        days_remaining = (existing_cycle.end_date - timezone.now().date()).days + 1
        if days_remaining > 0:
            total_spent = Expense.objects.filter(
                user=request.user, cycle=existing_cycle
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            remaining  = existing_cycle.total_allowance - total_spent
            preview_daily_limit = remaining / days_remaining

    return render(request, 'expenssesApp/setCycle.html', {
        'form':                form,
        'existing_cycle':      existing_cycle,
        'preview_daily_limit': preview_daily_limit,
    })


# ── User Story 3: Visual Spending Insights ───────────────────────────────────
@login_required(login_url='login')
def spendingInsights(request):
    """
    Shows a visual breakdown of expenses by category for the active cycle
    using a pure-CSS horizontal bar chart — no JavaScript required.
    All percentages and amounts are computed server-side.
    """
    cycle         = Cycle.objects.filter(user=request.user, is_active=True).first()
    chart_labels  = []
    chart_data    = []
    chart_colors  = []
    total_spent   = Decimal('0.00')
    category_rows = []

    COLORS = [
        '#6366f1', '#f59e0b', '#10b981', '#ef4444', '#3b82f6',
        '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#84cc16',
    ]

    if cycle:
        total_spent = (
            Expense.objects
            .filter(user=request.user, cycle=cycle)
            .aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        )

        expenses_by_category = (
            Expense.objects
            .filter(user=request.user, cycle=cycle)
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        for idx, row in enumerate(expenses_by_category):
            color      = COLORS[idx % len(COLORS)]
            amount     = row['total']
            percentage = round(float(amount / total_spent * 100), 1) if total_spent > 0 else 0.0

            chart_labels.append(row['category__name'])
            chart_data.append(float(amount))
            chart_colors.append(color)
            category_rows.append({
                'name':       row['category__name'],
                'amount':     amount,
                'percentage': percentage,
                'color':      color,
            })

    return render(request, 'expenssesApp/spendingInsights.html', {
        'cycle':         cycle,
        'total_spent':   total_spent,
        'category_rows': category_rows,
    })

@login_required(login_url='login')
def category_list(request):
    categories = Category.objects.filter(user=request.user).order_by('name')
    return render(request, 'expenssesApp/category_list.html', {
        'categories': categories
    })


@login_required(login_url='login')
def edit_category(request, category_id):
    """Edit existing category"""
    category = Category.objects.get(id=category_id, user=request.user)
    
    if request.method == "POST":
        form = categoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = categoryForm(instance=category)
    
    return render(request, 'expenssesApp/edit_category.html', {
        'form': form,
        'category': category
    })



@login_required(login_url='login')
def delete_category(request, category_id):
    """Delete a category"""
    category = Category.objects.get( id=category_id, user=request.user)
    
    if request.method == "POST":
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'expenssesApp/delete_category.html', {'category': category})