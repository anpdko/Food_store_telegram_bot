from .models import Order
from django.forms import ModelForm, fields, TextInput, NumberInput



class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['nameUser', 'phone']

        widgets = {
            "nameUser": TextInput(attrs={
                "placeholder": "Ім'я",
                "class": "form-control"
            }),
            "phone": TextInput(attrs={
                "placeholder": "Номер телефону",
                "class": "form-control",
                "pattern": "^\+380\d{9}$",
                "title": "Только в таком формате, например: +380677686921"
            })
        }