from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from .forms import UserEditForm


@login_required
def profile(request):
    if request.method == "POST":
        form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your information has been updated!"))
            return redirect("users:profile")
    else:
        form = UserEditForm(instance=request.user)

    context = {"form": form}

    return render(request, "users/profile.html", context=context)
