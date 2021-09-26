from django.urls import path, re_path
from tickets.views import *
# WelcomeView, MenuView, TicketView, OpsView, NextView


urlpatterns = [
    path('welcome/', WelcomeView.as_view()),
    path('menu', MenuView.as_view()),
    re_path(r'get_ticket/\w', TicketView.as_view()),
    path('processing', OpsView.as_view()),
    path('next', NextView.as_view(), name='next')
]
