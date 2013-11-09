from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from lunch_economy.apps.core.models import Quote
from lunch_economy.apps.mail.models import Mail


def home(request):
    quote = Quote.get_random()
    context = RequestContext(request, {
        'quote': quote
    })
    return render(request, 'home.html', context)


def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('lunch_economy.apps.core.views.home')
        else:
            messages.error(request, "Account has been disabled.")
            return redirect('lunch_economy.apps.core.views.home')
    else:
        try:
            existing_user = User.objects.get(username=username)
        except User.DoesNotExist:
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Account has been created!")
            Mail.system_notification(
                recipient=new_user,
                text="Welcome to the site!"
            )
            return redirect('lunch_economy.apps.core.views.home')

        messages.error(request, "Invalid login or username already taken.")
        return redirect('lunch_economy.apps.core.views.home')


def log_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('lunch_economy.apps.core.views.home')