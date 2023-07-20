from django import template
from review.models import Review


register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def has_response(ticket):
    response = Review.objects.filter(ticket_id=ticket.id).all()
    if response:
        return True
    return False


@register.simple_tag(takes_context=True)
def get_author_display(context, user):
    if context['user'] == user:
        return 'vous'
    return user.username
