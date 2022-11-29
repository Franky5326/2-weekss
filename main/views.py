from urllib import request
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from .forms import RegisterUserForm, ApplicationCreateForm
from django.views import generic
from .models import Applications
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy


class IndexView(ListView):
    model = Applications
    paginate_by = 4

    def get_queryset(self):
        return Applications.objects.filter(status='ready')


def register(request):
    if request.method == 'POST':
        user_form = RegisterUserForm(request.POST)
        if user_form.is_valid():
            # Создаем объект, но пока не сохраняем
            new_user = user_form.save(commit=False)
            # устанавливаем пароль
            new_user.set_password(user_form.cleaned_data['password1'])
            # Сохраняем пользователя
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})

    else:
        user_form = RegisterUserForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def profile(request):
    return render(
        request,
        'registration/profile.html'
    )


class ViewApplications(generic.ListView):
    model = Applications
    paginate_by = 3
    template_name = 'accounts/application_list.html'
    context_object_name = 'da'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Applications.objects.filter()
        else:
            return Applications.objects.filter(user__exact=self.request.user.id)


class CreateApplication(CreateView):
    model = Applications
    fields = ('title', 'desc', 'img')
    template_name = 'accounts/application_form.html'

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.user = self.request.user
        fields.save()

        return super().form_valid(form)


class DetailApplication(DetailView):
    model = Applications
    template_name = 'accounts/application_detail.html'


class DeleteApplication(DeleteView):
    model = Applications
    success_url = reverse_lazy('profile_applications')
    template_name = 'accounts/application_confirm_delete.html'


class UpdateApplication(UpdateView):
    model = Applications
    fields = ('status', 'category')
    template_name = 'accounts/application_form.html'
