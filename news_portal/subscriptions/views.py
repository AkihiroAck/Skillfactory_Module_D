from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from mymodel.models import Category
from .models import Subscriptions

# Create your views here.


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        action = request.POST.get('action')
        if action == 'subscribe':
            Subscriptions.objects.create(
                user=request.user,
                category=Category.objects.get(pk=category_id)
            )
        elif action == 'unsubscribe':
            Subscriptions.objects.filter(
                user=request.user,
                category_id=category_id
            ).delete()
        
        return redirect('subscriptions')  # Переадресация для предотвращения повторной отправки формы
    
    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriptions.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    
    context = {
        'user': request.user,
        'categories': categories_with_subscriptions,
    }
    
    return render(
        request,
        'subscriptions.html',
        context,
    )
