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
    followeds = get_followeds(user)
    for followed in followeds:
        reviews = models.Review.objects.filter(
            user=followed
        )
        for review in list(reviews):
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

    return all_tickets
