from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView


from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать в наш сервис!"
        message = "Спасибо за регистрацию!"
        from_email = "ng_nl01@mail.ru"
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)
