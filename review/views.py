from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def hello_world(request):
    return render(request,
                  'review/hello.html'
                  )

