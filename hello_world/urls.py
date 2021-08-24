from django.urls import path
from . import views

urlpatterns = [
             path('rps/<int:gameId>/', views.returnGameState, name='returnGameState'),
             path('rps/<int:gameId>/left/<int:handCode>/', views.setLeft, name='setLeft'),
             path('rps/<int:gameId>/right/<int:handCode>/', views.setRight, name='setRight'),
             path('rps/<int:gameId>/evaluate/', views.evaluate, name='evaluateGame'),
             path('rps/<int:gameId>/reset/', views.reset, name='resetGame'),
             path('rps/<int:gameId>/checkId/', views.checkId, name='checkId'),
             path('rps/createGame/', views.createGame, name='createGame'),
             path('', views.index, name='index'),
             ]
