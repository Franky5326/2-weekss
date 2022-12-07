from django.shortcuts import render
from .forms import RegisterUserForm, CategoryForm
from .models import Applications, Category
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from .filters import CategoryFilters
from django.contrib.auth.decorators import login_required


def IndexView(request):
    f = CategoryFilters(request.GET, queryset=Applications.objects.filter(status='ready'))
    return render(request, 'users/home.html', {'filter': f})


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


class DeleteCategoryView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_control')
    template_name = 'accounts/delete_category.html'


def profile(request):
    return render(
        request,
        'registration/profile.html'
    )


class ViewApplications(ListView):
    model = Applications
    paginate_by = 3
    template_name = 'accounts/application_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Applications.objects.filter()
        else:
            return Applications.objects.filter(user__exact=self.request.user.id)




@login_required
def my_post(request):
    f = CategoryFilters(request.GET, queryset=Applications.objects.filter(status='ready'))
    return render(request, 'accounts/application_list.html', {'filter': f})


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


class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'accounts/create_category.html'
    success_url = reverse_lazy('category_control')


class CategoryControl(ListView):
    model = Category
    template_name = 'accounts/category_control.html'
