from django.shortcuts import render
from .models import *
from django.http import FileResponse, Http404

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login




def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Vérifie si le nom d'utilisateur existe
        if not CustomUser.objects.filter(username=username).exists():
            return render(request, 'connexion.html', {'error': "Nom incorrect."})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirection selon le rôle
            return redirect('acceuil')

        else:
            return render(request, 'connexion.html', {'error': "Mot de passe incorrect."})

    return render(request, 'connexion.html')

CustomUser = get_user_model()

def inscription(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'inscription.html', {'error': "Les mots de passe ne correspondent pas."})

        try:
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password1),
                role='etudiant' 
            )
            return redirect('connexion')
        except IntegrityError:
            return render(request, 'inscription.html', {'error': "Ce nom d'utilisateur existe déjà."})

    return render(request, 'inscription.html')



def profil_view(request):
    return render(request, 'profile.html')


def modifier_profil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, "Profil mis à jour avec succès.")
    return redirect('profil')
    

def accueil_public(request):
    return render(request, 'accueil_public.html')  # page simple avec image et navbar

    

def acceuil(request):
    liste_categorie = Categorie.objects.all()
    requete = ""
    categorie_id = ""
    liste_livres = Book.objects.filter(valide=True)

    if request.method == "POST":
        if 'title' in request.POST and 'author' in request.POST:
            # Formulaire d'ajout de livre
            title = request.POST.get('title')
            author = request.POST.get('author')
            cover = request.FILES.get('cover')
            pdf = request.FILES.get('pdf')
            cat_id = request.POST.get('categorie')

            if not all([title, author, cover, pdf, cat_id]):
                messages.error(request, "Tous les champs du formulaire sont obligatoires.")
            else:
                try:
                    categorie = Categorie.objects.get(id=cat_id)
                    Book.objects.create(
                        title=title,
                        author=author,
                        cover=cover,
                        pdf=pdf,
                        categorie=categorie,
                        valide=False  # 🛑 Important : On force valide à False
                    )
                    messages.success(request, "Livre envoyé, en attente de validation.")
                    return redirect('acceuil')
                except Categorie.DoesNotExist:
                    messages.error(request, "Catégorie invalide.")
                except Exception as e:
                    messages.error(request, f"Erreur : {e}")
        else:
            # Traitement de la recherche ou du filtre
            requete = request.POST.get('requete', '')
            categorie_id = request.POST.get('categorie', '')

            livres_filtres = Book.objects.filter(valide=True)

            if requete:
                livres_filtres = livres_filtres.filter(
                    Q(title__icontains=requete) | Q(author__icontains=requete)
                )

            if categorie_id:
                livres_filtres = livres_filtres.filter(categorie_id=categorie_id)

            liste_livres = livres_filtres

    context = {
        'liste_livres': liste_livres,
        'liste_categorie': liste_categorie,
        'requete': requete,
        'categorie_id': categorie_id,
    }
    return render(request, 'acceuil.html', context)


@login_required
def ajouter_livre(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            livre = form.save(commit=False)
            livre.utilisateur = request.user  # ou auteur
            livre.valide = False  # le livre n’est PAS encore validé
            livre.save()
            messages.success(request, "Votre livre a été soumis. En attente de validation.")
            return redirect('acceuil')
    else:
        form = BookForm()
    return render(request, 'ajouter_livre.html', {'form': form})

@login_required
def adminPage(request):
    User = get_user_model() 
    nb_users = User.objects.count()
    nb_admins = User.objects.filter(role='admin').count()
    nb_books = Book.objects.count()
    nb_categories = Categorie.objects.count()

    context = {
        'nb_users': nb_users,
        'nb_admins': nb_admins,
        'nb_books': nb_books,
        'nb_categories': nb_categories
    }

    return render(request, 'adminPage.html', context)



@login_required
def gestion_utilisateurs(request):
    utilisateurs = CustomUser.objects.all()
    return render(request, 'gestion_utilisateurs.html', {'utilisateurs': utilisateurs})

@login_required
def supprimer_utilisateur(request, user_id):
    if request.user.is_superuser:  
        utilisateur = get_object_or_404(CustomUser, id=user_id)
        if utilisateur != request.user:  
            utilisateur.delete()
            messages.success(request, "Utilisateur supprimé avec succès.")
        else:
            messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
    else:
        messages.error(request, "Action non autorisée.")
    return redirect('gestion_utilisateurs')




@login_required
def gestion_categories(request):
    categories = Categorie.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'ajouter':
            nom = request.POST.get('nom')
            if nom:
                Categorie.objects.create(nom=nom)
                messages.success(request, "Catégorie ajoutée.")
                return redirect('gestion_categories')

        elif action == 'modifier':
            cat_id = request.POST.get('id')
            nom = request.POST.get('nom')
            categorie = get_object_or_404(Categorie, id=cat_id)
            if nom:
                categorie.nom = nom
                categorie.save()
                messages.success(request, "Catégorie modifiée.")
                return redirect('gestion_categories')

        elif action == 'supprimer':
            cat_id = request.POST.get('id')
            categorie = get_object_or_404(Categorie, id=cat_id)
            categorie.delete()
            messages.success(request, "Catégorie supprimée.")
            return redirect('gestion_categories')

    return render(request, 'gestion_categories.html', {'categories': categories})


@login_required
def gestion_livres(request):
    livres = Book.objects.select_related('categorie').all()
    categories = Categorie.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'ajouter':
            titre = request.POST.get('titre')
            auteur = request.POST.get('auteur')
            cat_id = request.POST.get('categorie')
            cover = request.FILES.get('cover')
            pdf = request.FILES.get('pdf')

            if titre and auteur and cat_id and cover and pdf:
                categorie = get_object_or_404(Categorie, id=cat_id)
                Book.objects.create(title=titre, author=auteur, cover=cover, pdf=pdf, categorie=categorie)
                messages.success(request, "Livre ajouté.")
                return redirect('gestion_livres')

        elif action == 'modifier':
            livre_id = request.POST.get('id')
            livre = get_object_or_404(Book, id=livre_id)
            titre = request.POST.get('titre')
            auteur = request.POST.get('auteur')
            cat_id = request.POST.get('categorie')
            cover = request.FILES.get('cover')
            pdf = request.FILES.get('pdf')

            if titre and auteur and cat_id:
                livre.title = titre
                livre.author = auteur
                livre.categorie = get_object_or_404(Categorie, id=cat_id)
                if cover:
                    livre.cover = cover
                if pdf:
                    livre.pdf = pdf
                livre.save()
                messages.success(request, "Livre modifié.")
                return redirect('gestion_livres')

        elif action == 'supprimer':
            livre_id = request.POST.get('id')
            livre = get_object_or_404(Book, id=livre_id)
            livre.delete()
            messages.success(request, "Livre supprimé.")
            return redirect('gestion_livres')

    return render(request, 'gestion_livres.html', {'livres': livres, 'categories': categories})

@login_required
def dashboard_etudiant(request):
    # On s’assure que l’utilisateur connecté est bien un étudiant
    if not hasattr(request.user, 'role') or request.user.role != 'etudiant':
        return redirect('acceuil')  # Redirection si ce n’est pas un étudiant

    # Comptages
    total_livres = Book.objects.count()
    total_categories = Categorie.objects.count()
    total_lecteurs = CustomUser.objects.filter(role='etudiant').count()

    # Comptage sans doublons (livres distincts)
    nb_consultations = Consultation.objects.filter(utilisateur=request.user).values('Book').distinct().count()
    nb_telechargements = Telechargement.objects.filter(utilisateur=request.user).values('Book').distinct().count()

    context = {
        'total_livres': total_livres,
        'total_categories': total_categories,
        'total_lecteurs': total_lecteurs,
        'nb_consultations': nb_consultations,
        'nb_telechargements': nb_telechargements,
    }

    return render(request, 'dashboard_etudiant.html', context)

@login_required
def promouvoir_admin(request, user_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('acceuil')

    utilisateur = get_object_or_404(CustomUser, id=user_id)
    
    if utilisateur.role != 'admin':
        utilisateur.role = 'admin'
        utilisateur.save()
        messages.success(request, "L'utilisateur a été promu au rôle admin.")
    
    return redirect('utilisateurs')

@login_required
def retirer_admin(request, user_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('acceuil')

    utilisateur = get_object_or_404(CustomUser, id=user_id)
    
    if utilisateur.role == 'admin':
        utilisateur.role = 'user'  # ou ce que tu utilises comme rôle "normal"
        utilisateur.save()
        messages.success(request, "Le rôle admin a été retiré à l'utilisateur.")
    
    return redirect('utilisateurs')


@login_required
def livres_en_attente(request):
    if request.user.role != 'admin':
        return redirect('acceuil')  # redirige les non-admins

    categories = Categorie.objects.all()
    return render(request, 'livres_en_attente.html', {
        'categories': categories,
    })


@login_required
def valider_ou_supprimer_livre(request, livre_id):
    if request.user.role not in ['admin', 'collaborateur']:
        return redirect('acceuil')

    livre = get_object_or_404(Book, id=livre_id)

    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'valider':
            livre.valide = True
            livre.save()
            messages.success(request, "Livre validé avec succès.")
        elif action == 'supprimer':
            livre.delete()
            messages.success(request, "Livre supprimé avec succès.")

    return redirect('livres_en_attente')

@login_required
def liste_utilisateurs(request):
    # ta logique pour afficher les utilisateurs
    utilisateurs = CustomUser.objects.all()
    return render(request, 'gestionutilisateur.html', {'utilisateurs': utilisateurs})

@login_required
def lire_livre(request, livre_id):
    livre = get_object_or_404(Book, id=livre_id)
    if livre.pdf:
        return FileResponse(livre.pdf.open('rb'), content_type='application/pdf')
    else:
        raise Http404("Fichier introuvable")


@login_required
def telecharger_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    if request.user.is_authenticated:
        Telechargement.objects.create(utilisateur=request.user, document=document)

    return FileResponse(document.fichier.open(), as_attachment=True, filename=document.fichier.name)

@login_required
def detail_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    # Enregistrer la consultation
    if request.user.is_authenticated:
        Consultation.objects.create(utilisateur=request.user, document=document)

    return render(request, 'detail_document.html', {'document': document})

@login_required
def consulter_livre(request, book_id):
    livre = get_object_or_404(Book, pk=book_id)
    if request.user.is_authenticated:
        Consultation.objects.create(utilisateur=request.user, Book=livre)

    return FileResponse(open(livre.pdf.path, 'rb'), content_type='application/pdf')

@login_required
def telecharger_livre(request, book_id):
    livre = get_object_or_404(Book, pk=book_id)
    if request.user.is_authenticated:
        Telechargement.objects.create(utilisateur=request.user, Book=livre)

    response = FileResponse(open(livre.pdf.path, 'rb'), as_attachment=True)
    return response
@login_required
def livres_consultes(request):
    consultations = Consultation.objects.filter(utilisateur=request.user)
    livres_uniques = list(set(c.Book for c in consultations))
    return render(request, 'livres_consultes.html', {'livres': livres_uniques})

@login_required
def livres_telecharges(request):
    telechargements = Telechargement.objects.filter(utilisateur=request.user)
    livres_uniques = list(set(t.Book for t in telechargements))
    return render(request, 'livres_telecharges.html', {'livres': livres_uniques})

def test_index_template(request):
    return render(request, 'index.html')