from review import models


def get_followeds(user):
    followed = []

    try:
        followings = models.UserFollows.objects.filter(
            user=user
        )
    except models.UserFollows.DoesNotExist:
        followings = None

    if followings:
        for userFollows in followings:
            followed.append(userFollows.followed_user)

    return followed


def get_user_viewable_reviews(user):
    all_reviews = []

    # Recupérer les critiques des utilisateurs suivis
    followeds = get_followeds(user)
    for followed in followeds:
        reviews = models.Review.objects.filter(
            user=followed
        )
        for review in list(reviews):
            all_reviews.append(review)

    # Récupérer les critiques du user connecté
    written = models.Review.objects.filter(
        user=user
    )

    for review in written:
        all_reviews.append(review)

    return all_reviews


def get_user_viewable_tickets(user):
    all_tickets = []
    followeds = get_followeds(user)
    for followed in followeds:
        tickets = models.Ticket.objects.filter(
            user=followed
        )
        for ticket in list(tickets):
            all_tickets.append(ticket)

    # Récupérer les tickets du user connecté
    written = models.Ticket.objects.filter(
        user=user
    )

    for ticket in written:
        all_tickets.append(ticket)

    return all_tickets
