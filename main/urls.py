from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import IndexView, CreateCategoryView

urlpatterns = [
    path('', IndexView, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/applications', views.ViewApplications.as_view(), name='profile_applications'),
    path('profile/applications/create', views.CreateApplication.as_view(),
         name='profile_applications_create'),
    path('profile/applications/<int:pk>/', views.DetailApplication.as_view(),
         name='profile_application_detail'),
    path('profile/applications/<int:pk>/delete', views.DeleteApplication.as_view(),
         name='profile_application_delete'),
    path('profile/applications/<int:pk>/update', views.UpdateApplication.as_view(),
         name='profile_application_update'),
    path('create-category/', CreateCategoryView.as_view(), name='add_category'),
    path('category-control/',  staff_member_required(views.CategoryControl.as_view()),
         name='category_control'),
    path('delete-category/<int:pk>/', permission_required('change_post')(
        views.DeleteCategoryView.as_view())
         , name='delete_category'),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/home/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
