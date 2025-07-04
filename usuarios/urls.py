from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('sair/', views.sair_view, name='sair'),
    path('cadastro/', views.register_view, name='cadastro'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('editar/', views.editar_perfil, name='editar_perfil'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='usuarios/password_reset_form.html'), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-completo/', auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), name='password_reset_complete'),
]
    