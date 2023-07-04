from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from review import forms
from django.contrib.auth import login


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'review/signup.html', context={'form': form})


@login_required
def hello_world(request):
    return render(request,
                  'review/hello.html'
                  )

