from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView

from .forms import MessageForm
from .models import Chat


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    context_object_name = "chats"
    paginate_by = 25
    template_name = "chats/chats.html"

    def get_queryset(self):
        return Chat.objects.prefetch_related("participants").filter(
            participants=self.request.user
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context["active_chat"] = None

        return context


@login_required
def chat_details(request, pk):
    chat = get_object_or_404(Chat, pk=pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()

            return redirect(chat.get_absolute_url())
    else:
        form = MessageForm()

    context = {
        "form": form,
        "active_chat": chat,
        "chats": Chat.objects.prefetch_related("participants").filter(
            participants=request.user
        )[:25],
    }

    return render(request, "chats/chats.html", context=context)
