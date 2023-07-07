from django import template
from review.models import Review


register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__

@register.filter
def has_response(ticket):
    print(ticket)
    #     # reviews =
    response = Review.objects.filter(ticket_id=ticket.id).all()
    if response:
        return True
    # print('reponse :', response)
    return False