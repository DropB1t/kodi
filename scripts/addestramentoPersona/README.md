## topics mqtt
training/0000/0
training/idMacchina/idPersona
## imgStorer.py
Questo e' lo snippet di codice che salva le immagini all'interno di mongoDB. Nota:
```
CONNECTION_STRING = "mongodb://root:root@localhost:27017/"
                            /             \
                           |usrname:password|
```
Per ora le foto vengono salvate una ad una e sembra che tutto vada bene anche mandando numerose foto
una dietro l'altra. Nota pero' che al posto di usare "insert_one" si puo' anche usare "insert_many"
chi inserisce piu' documenti all'interno della collection.
Questo script prendi in INPUT le immagini encodate come per riconoscimentoPersona e salva su mongoDB
seguendo questo albero:
```
trainingDatabase
├── 0000
│   ├── 0
│   │   ├── foto1
│   │   ├── foto2
│   │   └── ...
│   ├── 1
│   ├── 2
│   ├── 3
│   └── ...
├── 0001
│   ├── 0
│   ├── 1
│   └── ...
└── ...
```
Dove:
+ 0000, 0001 ... sono gli id delle macchine
+ 0, 1, ... sono gli id delle persone
+ foto sono file json di questo tipo:
```
foto = {
            "foto_id" : startingId+1,
            "foto" : img
}
```
Dove l'id e' generato in modo progressivo. Forse l'id non serve ma per sicurezza l'ho messo

## imgRetriever.py
E' incompleto perche' non so come salvare le foto. Se si passeranno come array allo script di addestramento
questo snippet andra' integrato a quello di addestramento. In caso invece si salvino in cartelle temporanee 
si puo' usare gli script come sono ora.
## imgSender.py
Manda foto 48x48 grayScale nella cartella ./img
## modelGenerator.py
Genera il modello. Nota che il parametro 2 nel layer denso finale dipende da quante persone bisogna addestrare
quindi nello script finale bisogna detectare o il numero di cartelle o il numero di persone diverse nell'array
## trainer.py
Quello che effettivamente addestra il modello e genera i pesi. 
