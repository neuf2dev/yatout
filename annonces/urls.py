from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil_annonces, name='accueil_annonces'),
    path('deposer/', views.deposer_annonce, name='deposer_annonce'),
    path('annonce/<int:pk>/', views.detail_annonce, name='detail_annonce'),
    path('annonce/<int:pk>/modifier/', views.modifier_annonce, name='modifier_annonce'),
    path('annonce/<int:pk>/supprimer/', views.supprimer_annonce, name='supprimer_annonce'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='logout'),
    path('mes-annonces/', views.mes_annonces, name='mes_annonces'),
    path('mes-favoris/', views.mes_favoris, name='mes_favoris'),
    path('favori/toggle/<int:pk>/', views.toggler_favori, name='toggler_favori'),
    path('mes-messages/', views.mes_messages, name='mes_messages'),
    path('envoyer-message/<int:pk>/', views.envoyer_message, name='envoyer_message'),
    path('mon-compte/', views.mon_compte, name='mon_compte'),
    path('mes-recherches/', views.mes_recherches, name='mes_recherches'),
]