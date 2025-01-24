from django.urls import path
from chat import views as chat_views

urlpatterns = [
    
  path("auth/login/", chat_views.login_user, name="login"),
    path("auth/logout/", chat_views.logout_user, name="logout"),
    path("auth/register/", chat_views.register_user, name="register"),
    path("users/", chat_views.get_users, name="get_users"),  # Fetch all users
    path("chat-history/", chat_views.get_chat_history, name="get_chat_history"),  # Fetch chat history
]