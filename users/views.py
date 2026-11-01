from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models import User

class RegisterView(CreateView):
    """Регистрация пользователя с отправкой приветственного письма."""
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)

        send_mail(
            subject="Добро пожаловать в Skystore!",
            message=(
                f"Здравствуйте, {self.object.username}!\n\n"
                f"Спасибо за регистрацию в Skystore.\n"
                f"Ваш email: {self.object.email}\n\n"
                f"Приятных покупок!"
            ),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[self.object.email],
            fail_silently=True,
        )

        return response


class UserLoginView(DjangoLoginView):
    """Вход по email и паролю."""
    form_class = UserLoginForm
    template_name = "users/login.html"


class UserLogoutView(DjangoLogoutView):
    """Выход из аккаунта."""
    next_page = reverse_lazy("catalog:home")

class UserProfileView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля текущего пользователя."""
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        # Редактируем всегда текущего пользователя, а не по pk из URL
        return self.request.user