from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Annonce, Favori, Message

# 1. Page d'accueil avec moteur de recherche + PAGINATION + CATEGORIES DYNAMIQUES
def accueil_annonces(request):
    annonces_list = Annonce.objects.all().order_by('-date_publication')
    
    query = request.GET.get('q')
    categorie = request.GET.get('categorie')
    ville = request.GET.get('ville')
    titre_seulement = request.GET.get('titre_seulement')

    if query:
        if titre_seulement:
            annonces_list = annonces_list.filter(titre__icontains=query)
        else:
            annonces_list = annonces_list.filter(
                Q(titre__icontains=query) | Q(description__icontains=query)
            )

    if categorie:
        annonces_list = annonces_list.filter(categorie=categorie)

    if ville:
        annonces_list = annonces_list.filter(ville__icontains=ville)

    paginator = Paginator(annonces_list, 4) 
    page_number = request.GET.get('page')
    annonces = paginator.get_page(page_number)

    # Récupération dynamique des catégories définies dans le modèle Annonce
    categories = getattr(Annonce, 'CATEGORIES', getattr(Annonce, 'CATEGORIE_CHOICES', []))

    context = {
        'annonces': annonces,
        'categories': categories,
    }

    return render(request, 'annonces/accueil.html', context)

# 2. Formulaire pour déposer une annonce
@login_required(login_url='connexion')
def deposer_annonce(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        categorie = request.POST.get('categorie')
        prix = request.POST.get('prix')
        description = request.POST.get('description')
        ville = request.POST.get('ville')
        telephone = request.POST.get('telephone')
        image = request.FILES.get('image')

        Annonce.objects.create(
            auteur=request.user,
            titre=titre,
            categorie=categorie,
            prix=prix,
            description=description,
            ville=ville,
            telephone=telephone,
            image=image
        )
        return redirect('mes_annonces')

    return render(request, 'annonces/deposer.html')

# 3. Page de détail d'une annonce
def detail_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    
    annonce.vues += 1
    annonce.save()

    messages = None
    if request.user.is_authenticated:
        messages = Message.objects.filter(annonce=annonce).filter(
            Q(expediteur=request.user) | Q(destinataire=request.user)
        ).order_by('date_envoi')

    return render(request, 'annonces/detail.html', {'annonce': annonce, 'messages': messages})

# 4. Inscription d'un nouvel utilisateur
def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil_annonces')
    else:
        form = UserCreationForm()
    
    return render(request, 'annonces/inscription.html', {'form': form})

# 5. Liste des annonces de l'utilisateur connecté
@login_required(login_url='connexion')
def mes_annonces(request):
    annonces = Annonce.objects.filter(auteur=request.user).order_by('-date_publication')
    return render(request, 'annonces/mes_annonces.html', {'annonces': annonces})

# 6. Supprimer une annonce
@login_required(login_url='connexion')
def supprimer_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk, auteur=request.user)
    if request.method == 'POST':
        annonce.delete()
    return redirect('mes_annonces')

# 7. Page de connexion
def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accueil_annonces')
    else:
        form = AuthenticationForm()
    return render(request, 'annonces/connexion.html', {'form': form})

# 8. Modifier une annonce
@login_required(login_url='connexion')
def modifier_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk, auteur=request.user)

    if request.method == 'POST':
        annonce.titre = request.POST.get('titre')
        annonce.categorie = request.POST.get('categorie')
        annonce.prix = request.POST.get('prix')
        annonce.description = request.POST.get('description')
        annonce.ville = request.POST.get('ville')
        annonce.telephone = request.POST.get('telephone')

        if request.FILES.get('image'):
            annonce.image = request.FILES.get('image')

        annonce.save()
        return redirect('mes_annonces')

    return render(request, 'annonces/modifier.html', {'annonce': annonce})

# 9. Ajouter / Retirer un favori
@login_required(login_url='connexion')
def toggler_favori(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    favori, created = Favori.objects.get_or_create(utilisateur=request.user, annonce=annonce)

    if not created:
        favori.delete()

    return redirect(request.META.get('HTTP_REFERER', 'accueil_annonces'))

# 10. Page Mes Favoris
@login_required(login_url='connexion')
def mes_favoris(request):
    favoris = Favori.objects.filter(utilisateur=request.user).select_related('annonce')
    return render(request, 'annonces/mes_favoris.html', {'favoris': favoris})

# 11. Envoyer un message depuis la fiche annonce
@login_required(login_url='connexion')
def envoyer_message(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            Message.objects.create(
                annonce=annonce,
                expediteur=request.user,
                destinataire=annonce.auteur,
                contenu=contenu
            )
            
    return redirect('detail_annonce', pk=annonce.pk)

# 12. Page Mes Messages
@login_required(login_url='connexion')
def mes_messages(request):
    messages = Message.objects.filter(
        Q(destinataire=request.user) | Q(expediteur=request.user)
    ).select_related('annonce', 'expediteur', 'destinataire').order_by('-date_envoi')
    
    return render(request, 'annonces/mes_messages.html', {'messages': messages})

# 13. Page Mon Compte / Tableau de bord profil
@login_required(login_url='connexion')
def mon_compte(request):
    nb_annonces = Annonce.objects.filter(auteur=request.user).count()
    nb_favoris = Favori.objects.filter(utilisateur=request.user).count()
    nb_messages = Message.objects.filter(
        Q(destinataire=request.user) | Q(expediteur=request.user)
    ).count()

    context = {
        'nb_annonces': nb_annonces,
        'nb_favoris': nb_favoris,
        'nb_messages': nb_messages,
    }
    return render(request, 'annonces/mon_compte.html', context)

# 14. Déconnexion
def deconnexion(request):
    logout(request)
    return redirect('accueil_annonces')