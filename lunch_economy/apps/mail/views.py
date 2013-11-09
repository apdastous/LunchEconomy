from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from lunch_economy.apps.mail.models import Mail


@login_required
def inbox(request):
    mail = Mail.objects.filter(recipient=request.user.id).order_by('-id')
    context = RequestContext(request, {
        'mail': mail
    })

    return render(request, 'inbox.html', context)


@login_required
def mail_detail(request, mail_id):
    mail = get_object_or_404(Mail, pk=mail_id)
    mail.read = True
    mail.save()
    context = RequestContext(request, {
        'mail': mail
    })

    return render(request, 'mail_detail.html', context)