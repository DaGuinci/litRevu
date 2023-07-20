from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError

from itertools import chain

from review import forms
from review import models
from review import tools


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
                messages.error(request,
                               'Nom d\'utilisateur ou mot de passe incorrect')
                return redirect('login')
    return render(request, 'review/login.html', context={'form': form})


@login_required
def home(request):
    reviews = tools.get_user_viewable_reviews(request.user)

    if len(reviews) > 0:
        # préparer des iterateurs pour les etoiles dans le html
        for review in reviews:
            review.rate_iterator = range(review.rating)
            review.unrate_iterator = range(5 - review.rating)

    tickets = tools.get_user_viewable_tickets(request.user)

    posts = sorted(
        chain(reviews, tickets),
        key=lambda instance: instance.time_created,
        reverse=True
        )
    return render(request,
                  'review/home.html',
                  {'posts': posts,
                   'animation': True}
                  )


@login_required
def user_posts(request):
    reviews = tools.get_user_reviews(request.user)
    tickets = tools.get_user_tickets(request.user)

    if len(reviews) > 0:
        # préparer des iterateurs pour les etoiles dans le html
        for review in reviews:
            review.rate_iterator = range(review.rating)
            review.unrate_iterator = range(5 - review.rating)

    posts = sorted(
        chain(reviews, tickets),
        key=lambda instance: instance.time_created,
        reverse=True
        )
    return render(request,
                  'review/user_posts.html',
                  {'posts': posts}
                  )


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


@login_required
def add_review_to(request, ticket_id):
    form = forms.CreateReviewForm()
    ticket = models.Ticket.objects.get(id=ticket_id)

    # Vérifier qu'aucun utilisateur n'a dèjá répondu
    try:
        ticket_has_response = models.Review.objects.get(
            ticket_id = ticket_id
        )
    except models.Review.DoesNotExist:
        ticket_has_response = False

    if not ticket_has_response:
        if request.method == 'POST':
            form = forms.CreateReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.ticket_id = ticket_id
                review.save()
                return redirect('home')
        return render(request, 'review/add_review.html', context={
            'review_form': form,
            'ticket': ticket
            })
    else:
        messages.error(
            request,
            'Ce billet a déjà été traité.'
                )
        return redirect('home')


@login_required
def edit_review(request, id):
    review = models.Review.objects.get(
        id=id
    )

    if review.user == request.user:

        if request.method == 'POST':
            form = forms.CreateReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = forms.CreateReviewForm(instance=review)

        return render(request,
                      'review/edit_post.html',
                      {'form': form}
                      )

    else:
        return home(request)


@login_required
def delete_review(request, id):
    review = models.Review.objects.get(
        id=id
    )

    if review.user == request.user:
        if request.method == 'POST':
            review.delete()
            return render(request,
                          'review/delete_success.html',
                          {'post': review}
                          )
        else:
            return render(request,
                          'review/delete_confirm.html',
                          {'review': review}
                          )

    else:
        return home(request)


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
def edit_ticket(request, id):
    ticket = models.Ticket.objects.get(
        id=id
    )

    if ticket.user == request.user:

        if request.method == 'POST':
            form = forms.CreateTicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = forms.CreateTicketForm(instance=ticket)

        return render(request,
                      'review/edit_post.html',
                      {'form': form}
                      )

    else:
        return home(request)


@login_required
def delete_ticket(request, id):
    ticket = models.Ticket.objects.get(
        id=id
    )

    if ticket.user == request.user:
        if request.method == 'POST':
            ticket.delete()
            return render(request,
                          'review/delete_success.html',
                          {'post': ticket}
                          )
        else:
            return render(request,
                          'review/delete_confirm.html',
                          {'ticket': ticket}
                          )

    else:
        return home(request)


@login_required
def subscribes(request):
    form = forms.UserFollowForm()

    # Obtenir la liste des abonnés
    followers = []

    try:
        followerings = models.UserFollows.objects.filter(
            followed_user=request.user
        )
    except models.UserFollows.DoesNotExist:
        followerings = None

    for follower in followerings:
        followers.append(follower.user)

    # Obtenir la liste des abonnements
    followed = tools.get_followeds(request.user)

    if request.method == 'POST':
        form = forms.UserFollowForm(request.POST)
        if form.is_valid():

            # Verifier si la demande est une subscription ou un désabonnement
            if 'to_follow' in request.POST:
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

                    userFollows = models.UserFollows(
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

            # cas de desabonnement
            else:
                try:
                    unfollowedName = request.POST['username']
                    unfollowed = User.objects.get(
                        username=unfollowedName
                    )

                    following = models.UserFollows.objects.get(
                        followed_user=unfollowed,
                        user=request.user
                    )

                    following.delete()
                    return redirect('subscribes')

                except models.UserFollows.DoesNotExist:
                    pass

    return render(request, 'review/subscribes.html', context={
        'form': form,
        'followed': followed,
        'followers': followers
        })
