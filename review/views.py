from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError

from itertools import chain

from review import forms
from review.models import Review, Ticket, UserFollows


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
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
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
    review_form = forms.CreateReviewForm()
    ticket_form = forms.CreateTicketForm()
    if request.method == 'POST':
        review_form = forms.CreateReviewForm(request.POST)
        ticket_form = forms.CreateTicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    return render(request, 'review/add_review.html', context={
        'review_form': review_form,
        'ticket_form': ticket_form
        })

def add_review_to(request, ticket_id):
    form = forms.CreateReviewForm()
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        form = forms.CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            # TODO populate ticket
            review.ticket_id = ticket_id
            review.save()
            return redirect('home')
    return render(request, 'review/add_review.html', context={
        'review_form': form,
        'ticket': ticket
        })

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

@login_required
def subscribes(request):
    form = forms.UserFollowForm()

    # Obtenir la liste des abonnés
    followers = []

    try:
        followerings = UserFollows.objects.filter(
            followed_user=request.user
        )
    except UserFollows.DoesNotExist:
        followerings = None

    for follower in followerings:
        followers.append(follower.user)

    # Obtenir la liste des abonnements
    followed = []

    try:
        followings = UserFollows.objects.filter(
            user=request.user
        )
    except UserFollows.DoesNotExist:
        followings = None

    for userFollows in followings:
        followed.append(userFollows.followed_user)

    if request.method == 'POST':
        form = forms.UserFollowForm(request.POST)
        if form.is_valid():
            # Vérifier que l'utilisateur ne se suit pas lui-meme
            if form.cleaned_data['to_follow'] != request.user.username:
                # Vérifier que l'utilisateur existe
                try:
                    to_follow = User.objects.get(
                        username=form.cleaned_data['to_follow']
                    )
                except User.DoesNotExist:
                    messages.error(
                        request,
                        'Nous ne connaissons pas cet utilisateur, \
                            veuillez essayer un autre nom.'
                            )
                    return redirect('subscribes')


                userFollows = UserFollows(
                    user=request.user,
                    followed_user=to_follow
                    )

                # Vérifier que l'utilisateur n;est pas déjà suivi
                try:
                    userFollows.save()
                except IntegrityError:
                    messages.error(
                        request,
                        'Vous suivez déjà cet utilisateur, \
                            veuillez essayer un autre nom.'
                            )
            else:
                messages.error(
                    request,
                    'Vous ne pouvez vous abonner à vous-même !')
            return redirect('subscribes')
    return render(request, 'review/subscribes.html', context={
        'form': form,
        'followed': followed,
        'followers': followers
        })

@login_required
def unfollow(request, username):

    try:
        unfollowed = User.objects.get(
            username=username
        )

        following = UserFollows.objects.get(
            followed_user=unfollowed,
            user=request.user
        )

        following.delete()

    except UserFollows.DoesNotExist:
        pass

    return subscribes(request)
