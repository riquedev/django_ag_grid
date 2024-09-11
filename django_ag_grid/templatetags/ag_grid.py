import itertools
from dynamic_preferences.users.forms import user_preference_form_builder
from django import template

register = template.Library()


@register.filter
def chunks(value, chunk_length):
    """
    Breaks a list up into a list of lists of size <chunk_length>
    """
    clen = int(chunk_length)
    i = iter(value)
    while True:
        chunk = list(itertools.islice(i, clen))
        if chunk:
            yield chunk
        else:
            break


@register.simple_tag(takes_context=True)
def field_notifications(context):
    request = context.get('request')
    if request:
        user = request.user
        return user.notifications.unread()


@register.inclusion_tag('field_ops/forms/user-preferences.html', takes_context=True)
def render_preferences_form(context):
    request = context.get('request')
    if request:

        context['next_url'] = request.path
        context['form'] = user_preference_form_builder(instance=request.user)

    return context
