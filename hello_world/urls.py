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
             path('loveletter/creategame/', views.createLoveLetterGame, name='createGameLoveLetter'),
             path('loveletter/gamestate/<int:gameId>/', views.loveLetterReturnGameState, name='loveLetterGameState'),
             path('loveletter/advanceturn/<int:gameId>/', views.advanceTurnLoveLetter, name='loveLetterAdvanceTurn'),
             path('loveletter/deal/<int:gameId>/<int:numberOfPlayers>/<int:deckNumber>', views.dealLoveLetter, name='loveLetterDeal'),
             path('loveletter/playCard/<int:gameId>/<str:card>/<int:playerNumber>/<int:target>/<str:guardGuess>/', views.playCardLoveLetter, name='loveLetterPlayCard'),
             path('loveletter/<int:gameId>/checkId/', views.checkIdLoveLetter, name='checkIdLoveLetter'),
             path('loveletter/<int:gameId>/resetGame/<int:deckNumber>/', views.resetGameLoveLetter, name='resetGameLoveLetter'),
             ]
