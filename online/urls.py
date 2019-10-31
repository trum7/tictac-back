from django.urls import path

from . import views

urlpatterns = [
    path('new/<slug:session>', views.new, name=''),
    path('games', views.games, name=''),
    path('join/<slug:session>', views.join, name=''),
    path('wait/<slug:session>', views.wait, name=''),
    path('play/<slug:session>', views.play, name=''),
    path('delete/<slug:session>', views.delete, name=''),
]
