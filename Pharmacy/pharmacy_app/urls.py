from django.urls import path
from . import views
from pharmacy_app.views import SignUpView, Dashboard, AddItem, EditItem, DeleteItem, ResetPasswordView, add_category, delete_category, EditCategory
from pharmacy_app.views import profile_view, update_profile, change_password_view, delete_user, logout_user
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.pharmacy_view, name='pharmacy_view'),
    path('signup/', SignUpView, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-category/', add_category, name='add-category'),
    path('edit-category/<int:pk>/', EditCategory.as_view(), name='edit-category'),
    path('delete-category/<int:category_id>/', delete_category, name='delete-category'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='passwordresetconfirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='passwordresetcomplete.html'),
         name='password_reset_complete'),
    path('profile/', profile_view, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),
    path('change-password/', change_password_view, name='change_password'),
    path('delete-user/', delete_user, name='delete_user'),
]
