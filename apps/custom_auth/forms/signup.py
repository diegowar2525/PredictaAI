from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from apps.custom_auth.validators.password import validar_password

User = get_user_model()


class SignUpForm(UserCreationForm):

    error_messages = {
        "password_mismatch": "Las contraseñas no coinciden",
    }

    first_name = forms.CharField(
        label="Nombre",
        required=True,
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre",
            "class": "bg-gray-200 px-3 py-2 outline-0 w-72 max-md:w-[70vw]"
        }),
        error_messages={
            "required": "El nombre es obligatorio",
            "min_length": "El nombre debe tener al menos 3 caracteres",
        }
    )

    last_name = forms.CharField(
        label="Apellido",
        required=True,
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={
            "placeholder": "Apellido",
            "class": "bg-gray-200 px-3 py-2 outline-0 w-72 max-md:w-[70vw]"
        }),
        error_messages={
            "required": "El apellido es obligatorio",
            "min_length": "El apellido debe tener al menos 3 caracteres",
        }
    )

    username = forms.CharField(
        label="Nombre de usuario",
        required=True,
        min_length=6,
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre de usuario",
            "class": "bg-gray-200 px-3 py-2 outline-0 w-72 max-md:w-[70vw]"
        }),
        error_messages={
            "required": "El nombre de usuario es obligatorio",
            "min_length": "El nombre de usuario debe tener al menos 6 caracteres",
        }
    )

    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Correo electrónico",
            "class": "bg-gray-200 px-3 py-2 outline-0 w-72 max-md:w-[70vw]"
        }),
        error_messages={
            "required": "El correo electrónico es obligatorio",
            "invalid": "Ingrese un correo electrónico válido",
        }
    )

    password1 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña",
            "class": "bg-gray-200 px-3 py-2 outline-0 w-72 max-md:w-[70vw]"
        }),
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirmar contraseña",
            "class": "bg-gray-200 px-3 py-2 outline-0 w-72 max-md:w-[70vw]"
        }),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

        error_messages = {
            "username": {
                "unique": "Este nombre de usuario ya está registrado",
            },
            "email": {
                "unique": "Este correo electrónico ya está registrado",
            },
        }

    def clean(self):
        cleaned_data = super().clean()

        # limpiar strings
        for campo in self.Meta.fields:
            valor = cleaned_data.get(campo)
            if isinstance(valor, str):
                cleaned_data[campo] = valor.strip()

        password1 = cleaned_data.get("password1")

        if password1:
            try:
                validar_password(password1)
                validate_password(password1)
            except ValidationError as e:
                self.add_error(None, e)  # 👈 error GLOBAL

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"].lower().strip()
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está registrado")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        if commit:
            user.save()
        return user
