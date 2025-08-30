from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

User = get_user_model()


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/registration.html'
    model = User
    success_url = reverse_lazy('quotes:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth.login(self.request, self.object)
        return response
