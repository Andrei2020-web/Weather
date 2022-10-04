from .models import City
from django.forms import ModelForm, TextInput
from django.core.exceptions import ValidationError

EMPTY_CITY_ERROR = "Пожалуйста, укажите название города."
DUPLICATE_CITY_ERROR = "Вы уже получили информацию по данному городу."
NON_EXISTENT_CITY_ERROR = "Информация по городу не найдена."


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

    def validate_unique(self):
        '''проверка уникальности'''
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'name': [DUPLICATE_CITY_ERROR]}
            self._update_errors(e)