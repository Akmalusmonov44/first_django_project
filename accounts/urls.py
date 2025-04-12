from django.contrib.auth.password_validation import password_changed
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

from news.views import admin_page_view
from .views import dashboard_view, user_register, SignUpView, edit_user, EditUserView, logout_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='register/', http_method_names = ['get', 'post', 'options']), name='logout'),
    path('logout/', logout_view, name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm' ),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', dashboard_view, name='user_profile'),
    path('signup/', SignUpView.as_view(), name='user_register'),
    path('signup/', user_register, name='user_register'),
    # path('profile/edit', edit_user, name='edit_user_information' )
    path('profile/edit', EditUserView.as_view(), name='edit_user_information' ),
    path('admin-page/', admin_page_view, name='admin_page' )


]
