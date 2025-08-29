from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import Quote, Source
from .forms import QuoteForm
import random

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Цитата успешно добавлена.')
            return redirect('quotes:random_quote')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        # Ошибки, не связанные с конкретными полями
                        messages.error(request, error)
                    else:
                        # Ошибки, связанные с конкретными полями
                        messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = QuoteForm()
    
    return render(request, 'quotes/add_quote.html', {'form': form})

def random_quote(request):
    quotes = Quote.objects.all()

    if quotes.exists():
        total_weight = sum(quote.weight for quote in quotes)
        random_value = random.randint(1, total_weight)
        cumulative_sum = 0
        for quote in quotes:
            cumulative_sum += quote.weight
            if cumulative_sum >= random_value:
                selected_quote = quote
                break
    else:
        selected_quote = None
    if selected_quote:
        selected_quote.views += 1
        selected_quote.save()

    return render(request, 'quotes/random_quote.html', {'quote': selected_quote})

def popular_quotes(request):
    sort_by = request.GET.get('sort_by', 'likes')

    if sort_by == 'dislikes':
        quotes = Quote.objects.all().order_by('-dislikes')[:10]
    elif sort_by == 'views':
        quotes = Quote.objects.all().order_by('-views')[:10]
    else:
        quotes = Quote.objects.all().order_by('-likes')[:10]

    return render(request, 'quotes/popular_quotes.html', {'quotes': quotes, 'sort_by': sort_by})

@login_required
def toggle_like_dislike(request, quote_id, action):
    quote = get_object_or_404(Quote, id=quote_id)
    if action == 'like':
        quote.likes += 1
    elif action == 'dislike':
        quote.dislikes += 1
    quote.save()
    return redirect('quotes:random_quote')