from django.urls import path
from chat import views as chat_views

urlpatterns = [
    
    path("auth/login/", chat_views.login_user, name="login-user"),
    path("auth/logout/", chat_views.logout_user, name="logout-user"),
     path("auth/register/", chat_views.register_user, name="register-user"),
]