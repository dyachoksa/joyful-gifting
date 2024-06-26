from django import template

from apps.chats.models import Chat


register = template.Library()


@register.filter
def chat_sender(chat: Chat, user):
    # note: participants should be prefetched to improve performance
    for participant in chat.participants.all():
        if participant.id != user.id:
            return participant

    return None
