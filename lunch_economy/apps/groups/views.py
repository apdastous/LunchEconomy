from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext

from lunch_economy.apps.groups.models import LunchGroup
from lunch_economy.apps.mail.models import Mail


def my_groups(request):
    groups = LunchGroup.objects.filter(user=request.user)
    context = RequestContext(request, {
        'groups': groups
    })
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
    all_groups = LunchGroup.objects.all()

    groups = []
    for group in all_groups:
        if not request.user in group.user_set.all():
            groups.append(group)

    context = RequestContext(request, {
        'groups': groups
    })
    return render(request, 'join_group.html', context)


def send_request(request, group_id):
    """
    Request to join via mail to a group leader.
    """
    group = get_object_or_404(LunchGroup, pk=group_id)
    Mail.objects.create(
        sender=request.user,
        recipient=group.leader,
        text="{0} wishes to join your group '{1}'.  Do you <a href='/groups/request/approve/{2}/{3}/'>approve</a>?".format(request.user.username, group.name, group.id, request.user.id)
    )
    messages.success(request, "Request has been sent to {0}.".format(group.leader.username))
    return redirect('join_group')


def approve_request(request, group_id, user_id):
    group = get_object_or_404(LunchGroup, pk=group_id, leader=request.user)
    user = get_object_or_404(User, pk=user_id)

    if group in user.groups.all():
        messages.warning(request, "{0} is already in the group '{1}'".format(user.username, group.name))
        return redirect('inbox')

    user.groups.add(group)
    Mail.objects.create(
        sender=request.user,
        recipient=user,
        text="You have joined the lunch group '{0}'.".format(group.name)
    )
    messages.success(request, "{0} has been added to the group '{1}'.".format(user.username, group.name))
    return redirect('inbox')