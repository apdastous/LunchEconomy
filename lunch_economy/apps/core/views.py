from django.shortcuts import render
from django.template import Context

from lunch_economy.apps.core.models import Quote


def home(request):
    quote = Quote.get_random()
    context = Context({
        'quote': quote
    })
    return render(request, 'home.html', context)