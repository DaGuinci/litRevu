from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from itertools import chain

from review import forms
from review.models import Review, Ticket

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


def log_user_in(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,'Nom d\'utilisateur ou mot de passe incorrect')
                return redirect('login')
    return render(request, 'review/login.html', context={'form': form})


@login_required
def home(request):
    # reviews = models.Review.objects.filter(
    #     uploader__in=request.user.follows.all()
    #     ).exclude(blog__in=blogs)
    reviews = Review.objects.all()

    # préparer des iterateurs pour les etoiles dans le html
    for review in reviews:
        review.rate_iterator = range(review.rating)
        review.unrate_iterator = range(5 - review.rating)

    tickets = Ticket.objects.all()

    posts = sorted(
        chain(reviews, tickets),
        key=lambda instance: instance.time_created,
        reverse=True
        )
    return render(request,
                  'review/home.html',
                  {'posts': posts}
                  )

# TODO ajouter argument id ticket pour si liaison ticket
@login_required
def add_review(request):
    form = forms.CreateReviewForm()
    if request.method == 'POST':
        form = forms.CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')
    return render(request, 'review/add_review.html', context={'form': form})

def add_review_to(request, ticket_id):
    form = forms.CreateReviewForm()
    if request.method == 'POST':
        form = forms.CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            # TODO populate ticket
            review.ticket_id = ticket_id
            review.save()
            return redirect('home')
    return render(request, 'review/add_review.html', context={'form': form})

@login_required
def add_ticket(request):
    form = forms.CreateTicketForm()
    if request.method == 'POST':
        form = forms.CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'review/add_ticket.html', context={'form': form})