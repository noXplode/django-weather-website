from .models import City
from django import forms
from django.utils.translation import gettext_lazy as _
from dal import autocomplete


class CityForm(forms.Form):
    picked_city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label='',
        widget=autocomplete.ModelSelect2(
            url='weatherapp:city-autocomplete',
            attrs={
                'data-placeholder': _('Введите город'),
                'data-minimum-input-length': 2,
                'data-theme': 'bootstrap4'
            }
        )
    )
