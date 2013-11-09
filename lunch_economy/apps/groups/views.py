from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext

from lunch_economy.apps.groups.models import LunchGroup
from lunch_economy.apps.mail.models import Mail


def my_groups(request):
    context = RequestContext(request, {})
    return render(request, 'my_groups.html', context)


def group_detail(request, group_id):
    group = get_object_or_404(LunchGroup, pk=group_id, leader=request.user)
    context = RequestContext(request, {
        'group': group,
    })
    return render(request, 'group_detail.html', context)


def create_group(request):
    if request.POST:
        group_name = request.POST['group-name']
        try:
            group = LunchGroup.objects.get(name=group_name)
        except LunchGroup.DoesNotExist:
            group = LunchGroup.objects.create(name=group_name, leader=request.user)
            group.save()
            request.user.groups.add(group)
            messages.success(request, "Group created!")
            Mail.system_notification(
                recipient=request.user,
                text="You have created a new group named '{0}'!".format(group.name)
            )
            return redirect('group_detail', group_id=group.id)

        messages.error(request, "Group name is already taken!")
        return redirect('create_group')
    else:
        context = RequestContext(request, {})
        return render(request, 'create_group.html', context)


def join_group(request):
    pass