from . import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    # followed = request.user.follows.all()
    return render(request, 'customUser/follow_users_form.html', context={
        'form': form})