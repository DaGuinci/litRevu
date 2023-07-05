from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from review import forms
from review.models import Review, Ticket
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
def home(request):
    # reviews = models.Review.objects.filter(
    #     uploader__in=request.user.follows.all()
    #     ).exclude(blog__in=blogs)
    reviews = Review.objects.all()
    tickets = Ticket.objects.all()
    return render(request,
                  'review/home.html',
                  {'reviews': reviews,
                   'tickets': tickets}
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