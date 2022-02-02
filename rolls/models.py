from django.db import models

# Create your models here.
class Roll(models.Model):
    immagine = models.ImageField()
    nome = models.CharField(max_length=20)
    prezzo = models.FloatField()

    def __str__(self):
        return self.nome