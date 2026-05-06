from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
from expensesApp.models import Cycle, Expense
from django.db.models import Sum


@login_required(login_url='login')
def home(request):
    """
    Home screen. Computes the Safe Daily Limit entirely on the server
    and passes it to the template — no JavaScript needed.

    Formula:
        remaining_budget = total_allowance - total_spent_so_far
        days_remaining   = end_date - today  (inclusive, min 1)
        safe_daily_limit = remaining_budget / days_remaining
    """
    context = {
        'cycle':            None,
        'safe_daily_limit': None,
        'total_spent':      Decimal('0.00'),
        'remaining_budget': None,
        'days_remaining':   None,
        'progress_percent': 0,
        'status':           'no_cycle',
        # الحقول الجديدة للتحذير
        'today_spent':      Decimal('0.00'),
        'over_daily_limit': False,
    }

    cycle = Cycle.objects.filter(user=request.user, is_active=True).first()

    if cycle:
        today = timezone.now().date()

        total_spent = (
            Expense.objects
            .filter(user=request.user, cycle=cycle)
            .aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        )

        remaining_budget = cycle.total_allowance - total_spent
        days_remaining   = max((cycle.end_date - today).days + 1, 1)
        safe_daily_limit = remaining_budget / Decimal(days_remaining)

        progress_percent = 0
        if cycle.total_allowance > 0:
            progress_percent = min(int(total_spent / cycle.total_allowance * 100), 100)

        if today > cycle.end_date:
            status = 'ended'
        elif remaining_budget < 0:
            status = 'overspent'
        else:
            status = 'active'

        # ---- حساب صرف اليوم ومقارنته بالحد الآمن ----
        today_spent = (
            Expense.objects
            .filter(user=request.user, cycle=cycle, time_stamp__date=today)
            .aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        )
        over_daily_limit = (today_spent > safe_daily_limit) if safe_daily_limit is not None else False

        context.update({
            'cycle':            cycle,
            'safe_daily_limit': safe_daily_limit,
            'total_spent':      total_spent,
            'remaining_budget': remaining_budget,
            'days_remaining':   days_remaining,
            'progress_percent': progress_percent,
            'status':           status,
            'today_spent':      today_spent,          # جديد
            'over_daily_limit': over_daily_limit,     # جديد
        })

    return render(request, 'main.html', context)