from lunch_economy.apps.mail.models import Mail


def unread_messages_notification(request):
    unread_messages = Mail.objects.filter(recipient=request.user.id, read=False)

    return {'unread_messages': unread_messages}