from django.urls import path
from .views import *
 
urlpatterns = [
   path('', bot, name="bot"),
   path('login', login, name='login'),
   path('register', register, name='register'),
   path('logout', logout, name='logout'),
   path('home/', home, name='home'),
   path('setting/', setting, name='setting'),
   path('profile/', profile, name="profile"),
   path('ask/', ask, name="ask"),

]