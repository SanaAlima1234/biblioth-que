from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import dashboard_etudiant



urlpatterns = [
    path('', views.accueil_public, name='accueil_public'),
    path('connexion', views.connexion, name="connexion"),
    path('acceuil', views.acceuil, name="acceuil"),
    
    path('inscription', views.inscription, name="inscription"),
    path('adminPage', views.adminPage, name="adminPage"),
    path('utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('utilisateurs/supprimer/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('categories/', views.gestion_categories, name='gestion_categories'),
    path('livres/', views.gestion_livres, name='gestion_livres'),
    path('profil/', views.profil_view, name='profil'),
    path('modifier-profil/', views.modifier_profil, name='modifier_profil'),
    path('logout/', LogoutView.as_view(next_page='connexion'), name='logout'),
    path('ajouter-livre/', views.ajouter_livre, name='ajouter_livre'),
    path('dashboarde/', dashboard_etudiant, name='dashboard_etudiant'),
    path('utilisateur/promouvoir/<int:user_id>/', views.promouvoir_admin, name='promouvoir_admin'),
    path('livres_en_attente/', views.livres_en_attente, name='livres_en_attente'),
    path('livres_en_attente/<int:livre_id>/', views.valider_ou_supprimer_livre, name='valider_ou_supprimer_livre'),
    path('utilisateur/retirer_admin/<int:user_id>/', views.retirer_admin, name='retirer_admin'),
    path('utilisateurs/', views.liste_utilisateurs, name='utilisateurs'),
    path('livre/lire/<int:livre_id>/', views.lire_livre, name='lire_livre'),
    path('livre/<int:book_id>/consulter/', views.consulter_livre, name='consulter_livre'),
    path('livre/<int:book_id>/telecharger/', views.telecharger_livre, name='telecharger_livre'),
    path('consulter/<int:book_id>/', views.consulter_livre, name='consulter_livre'),
    path('telecharger/<int:book_id>/', views.telecharger_livre, name='telecharger_livre'),
    path('mes-livres-consultes/', views.livres_consultes, name='livres_consultes'),
    path('mes-livres-telecharges/', views.livres_telecharges, name='livres_telecharges'),


]