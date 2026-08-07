# annonces/models.py

from django.db import models
from django.contrib.auth.models import User


class Annonce(models.Model):
    CATEGORIES = [
        ('VEHICULES', 'Véhicules'),
        ('IMMOBILIER', 'Immobilier'),
        ('AMEUBLEMENT', 'Ameublement'),
        ('DIVERS', 'Divers'),
    ]

    TYPE_CHOICES = [
        ('OFFRE', 'Offre'),
        ('DEMANDE', 'Demande'),
    ]

    # Nouveau champ
    type_annonce = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='OFFRE',
        verbose_name="Type d'annonce"
    )

    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annonces')
    titre = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORIES)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='annonces_photos/', blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    vues = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titre


class Favori(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoris')
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='favoris')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'annonce')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.annonce.titre}"


class Message(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.expediteur.username} à {self.destinataire.username} ({self.annonce.titre})"