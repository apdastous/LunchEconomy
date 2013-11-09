from django.shortcuts import render
from django.template import RequestContext

from lunch_economy.apps.core.models import Quote


def home(request):
    quote = Quote.get_random()
    context = RequestContext(request, {
        'quote': quote
    })
    return render(request, 'home.html', context)