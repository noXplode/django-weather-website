from django.template import Library
from django.urls import resolve, translate_url

register = Library()

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    path = context['request'].path
    return translate_url(path, lang)

