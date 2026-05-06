from django.urls import path
from .views import register,loginUser,logoutUser
urlpatterns = [
    path('register/',register,name='register'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),

]