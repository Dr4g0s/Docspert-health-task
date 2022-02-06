from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

from app.views import DashboardPageView, RegisterPageView
from app.forms import LoginForm


urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('dashboard'))),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('login/', 
        LoginView.as_view(
            template_name='login.html',
            authentication_form=LoginForm,
            redirect_authenticated_user=True
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
]