from django.contrib import admin
from django.urls import path,include

from UserAccount.forms import ResetPasswordForm, NewPasswordForm
from django.contrib.auth import views

urlpatterns = [
    path('',include('UserAccount.urls')),
    path('',include('Event.urls')),
    path('',include('Blood.urls')),
    path('',include('BBManager.urls')),
    path('',include('Nurse.urls')),
    path('',include('Hospital.urls')),
    path('',include('Donor.urls')),
    path('',include('LabTechnician.urls')),
    path('admin/', admin.site.urls , name='admin'),
    path('password-reset/', views.PasswordResetView.as_view(template_name="reset_password.html", form_class=ResetPasswordForm), name="password_reset"),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(template_name="reset_password_done.html"), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html", form_class=NewPasswordForm), name="password_reset_confirm"),
    path('password-reset-complete/', views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete"),
]
