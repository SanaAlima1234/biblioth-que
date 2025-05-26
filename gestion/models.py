from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 




class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers/')
    pdf = models.FileField(upload_to='books/')
    categorie = models.ForeignKey("Categorie", on_delete=models.CASCADE)
    valide = models.BooleanField(default=False)

    
    def __str__(self):
        return self.title




class CustomUser(AbstractUser):
   
    ROLE_CHOICES = (
        ('etudiant', 'Étudiant'),
        ('admin', 'Administrateur'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')

    def is_etudiant(self):
        return self.role == 'etudiant'

    def is_admin(self):
        return self.role == 'admin'

class Consultation(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_consultation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} a consulté {self.livre.title}"

class Telechargement(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_telechargement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} a téléchargé {self.livre.title}"