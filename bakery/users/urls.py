from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import RegisterUser, LoginUser, user_home

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('user_home/', user_home, name='user_home'),

]