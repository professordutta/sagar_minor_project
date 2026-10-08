from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.select_related('customer').order_by('-created_at')
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})

@login_required
def feedback_create(request):
    from customers.models import Customer
    customer = getattr(request.user, 'customer_profile', None)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            if customer:
                fb.customer = customer
            fb.save()
            return redirect('feedback:list')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})
