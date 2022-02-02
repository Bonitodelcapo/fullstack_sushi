python manage.py runserver      per far partire il sito
python manage.py startapp <nome_app>      per creare una nuova app

ppena creata una nuova app bisogna andare nella cartella parent (fullstack_sushi) e aprire settings.py 
Aggiungi rolls a "INSTALLED APPS"


INSTALLED_APPS = [
...
'rolls.apps.RollsConfig',
]


Adesso creiamo una "vista" o "view". Funziona secondo la logica di richiesta-risposta:
L'utente fa una richiesta tramite Url e la risposta è la pagina html/web richiesta.


in rolls/view.py:
def rolls(request):
    return render(request, 'rolls/sushi-rolls.html')   perche django checka gia nella cartella "template"/rolls/

IMPORTANTE ! IL CAZZO DI FILE HTML NON DEVE AVERE .html ALLA FINE DIO PORCO 

ESEMPIO MODULARE PER GLI urls:

in fullstack_sushi/urls.py :

from django.contrib import admin
from django.urls import path, include 
# from rolls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rolls/', include('rolls.urls')),
]


in rolls/urls.py  (se non presente, creare il file urls.py) :

from django.urls import path
from . import views

urlpatterns = [
     path('', views.rolls)
]


ADESSO CREIAMO UN MODELLO IN rolls/models.py PER POTER "SERIALIZZARE" LA CREAZIONE DELLE CARDS.
INFATTI SALVEREMO GLI ATTRIBUTI DELLE CARD IN UN DATABASE sqlite3.

in rolls/models.py

class Roll(models.Model):
    immagine = models.ImageField()
    nome = models.CharField(max_length=20)
    prezzo = models.FloatField()


Ora dobbiamo "avvertire" Django di tale modello attraverso una "migrazione".

Aprendo un nuovo terminale e runnando :

C:\Users\Gianluca\Desktop\fullstack_sushi>python manage.py makemigrations

e 

C:\Users\Gianluca\Desktop\fullstack_sushi>python manage.py migrate


Ora in pratica è stata creata la tabella del Database. ma come facciamo ad accedere al Database per inmserire i dati?

-> Attraverso la pagina 8000/admin 

come prima cosa pero bisogna creare un utente. Nel terminale digitiamo:

C:\Users\Gianluca\Desktop\fullstack_sushi>python manage.py createsuperuser

Username: <Username scelto da te> ES: admin
e-mail: <mail a scelta> Es: admin@example.com
Password: <Pass scelta da te> Es: admin

ora accediamo alla pagina con le credenziali create su.

Qui nell area di amministrazione possiamo gestire gli utenti e i dati nel database. La tabella del Database 
deve essere prima abilitata:

in rolls/admin.py:

from .models import Roll
admin.site.register(Roll)

Adesso dovrebbe essere comparsa una sezione "Rolls". cliccandoci sopra e poi su "add Roll" possiamo configurare
i Roll a nostro piacimento in modo piu modulare, senza dover scrivere tutto in html statico.

dopo aver inserito i parametri (immagine, nome e prezzo), clicchiamo su save. [saltiamola parte di definire il resto]

ora ci rendiamo conto che tutte l eimmagini caricate sono state copiate nella cartella root del progetto, sparse,
a cazzo di cane. Questo è scomodo e possiamo dire a Django dove le vogliamo salvare cosi:

in fullstack_sushi/settings.py

definiamo (in alto, ma non è importante dove) una nuova costante MEDIA_ROOT:

import os
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

in fullstack_sushi/urls.py modifichiamo come segue:

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rolls/', include('rolls.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


ora se andiamo a vedere i modelli "Rolls" creati, vengono mostrati (nel database) come "RollObject(1)",
"Rollobject(2)" etc. Per cambiare e far esi che vengano visualizzati con lìattributo nome modifichiamo cosi:

in rolls/models.py:

class Roll(models.Model):
    immagine = models.ImageField()
    nome = models.CharField(max_length=20)
    prezzo = models.FloatField()

    def __str__(self):
        return self.nome


        OGNI VOLTA CHE SI CAMBIANO I MODELLI BISOGNA GENERARE E APPLICARE LE MIGRAZIONI.

Adesso bisogna estrapolare i rolls dal database e passarli all apagina html che li deverenderizzare. Questa funzione 
è affidata alla "vista".


in rolls/views.py:

from . models import Roll

def rolls(request):
    rolls = Roll.objects.all()                                  // aggiunta questa 
    return render(request, 'rolls/sushi-rolls.html')  


    cosi facendo la variabile rolls contiene tutti i rolls nel database. Ora dobbiamo passarla alla pagina html:


def rolls(request):
    rolls = Roll.objects.all()
    return render(request, 'rolls/sushi-rolls.html', {'rolls' : rolls})    


in questo modo la pagina html potra accedere attraverso la chiave "rolls" (a sinistra) a tutti gli elementi
contenuti nell avariabile "rolls" (a destra) estrapolata dal database.

Django ci permette di scrivere codice django all'interno delle pagine html usando le parentesi graffe:

<!-- Container con le Cards-->
<div class="container">
  <div class="row">
      {% for roll in rolls %}
      <div class="col-sm">
        <div class="card" style="width: 18rem;">
          <img src="./images/california.png" class="card-img-top" alt="...">
          <div class="card-body">
            <h5 class="card-title">California Roll</h5>
            <p class="card-text">Questi sono i Roll preferiti di Pinesota che oggi a Best voleva prendere solo questi. Io non capisco perche sia cosi fissata, perche di Sushi non hanno niente, non essendo col pesce ma vegetariani !!!!</p>
            <a href="#" class="btn btn-primary">Aggiungi</a>
          </div>
        </div>
      </div>
      {% endfor %}


in questo modo abbiamo creato un ciclo che itera sugli elementi rolls presenti nel database.

utilizzando doppie graffe {{}} si possono definire varibili all interno di html. cosi facendo abbiamo utilizzato
ciclo for per assgnare a nome prezzo e immagine i rispettivi dati.

Cio che manca nella pagina adesso è il logo. Dato che il logo è un file statico, non ha troppo senso implementarlo
allo stesso modo dei rolls e inserirlo nel database. Django offre una buona modalità di gesitione dei file statici.

per prima cosa creiamo all' interno di rolls una nuova cartella "static". Al suo interno nuovamente una cartella 
con il nome della app (cioe rolls). All' intenro di rolls/static/rolls si troveranno tutti i file statici e 
Django è settato di default nell'andare a cercare all'intenro di questa cartella.

Dal desktop trasferiamo l'immagine del logo nella cartella appena creata.

Cambiamo il file html come segue per caricare la cartella static e definire il percorso per il logo:

<!-- Navbar con Image and text-->
<nav class="navbar navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        {% load static %}
        <img src="{% static 'rolls/logo.png' %}" alt="" width="30" height="24" class="d-inline-block align-text-top">
        Fullstack Sushi
      </a>
    </div>
</nav>




