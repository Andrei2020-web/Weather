from .models import City
from django.forms import ModelForm, TextInput

EMPTY_CITY_ERROR = "Пожалуйста, укажите название города."


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'name': 'city',
                                     'id': 'id_new_city',
                                     'placeholder': 'Введите город'})}

        error_messages = {
            'name': {'required': EMPTY_CITY_ERROR}
        }

