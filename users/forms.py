from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя."""

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Минимум 8 символов.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Введите пароль ещё раз.",
    )

    class Meta:
        model = User
        fields = ("email", "username", "avatar", "phone", "country")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя пользователя"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 999 123-45-67"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Россия"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Форма входа по email и паролю."""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ("email", "username", "avatar", "phone", "country")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email